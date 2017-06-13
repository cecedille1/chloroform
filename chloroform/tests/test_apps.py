# -*- coding: utf-8 -*-

import pytest
import django
try:
    from unittest import mock
except ImportError:
    import mock

from django.core.management import call_command

from chloroform.apps import after_saving_contact
from chloroform.models import Contact, Configuration


@pytest.mark.django_db
@pytest.mark.xfail(condition=django.VERSION < (1, 9),
                   reason='Django 1.8 has not transaction.on_commit')
def test_after_saving_contact():
    call_command('loaddata', 'chloroform/tests/test_apps.yaml')
    instance = Contact.objects.get(pk=1)
    with mock.patch('chloroform.mails.ChloroformMailBuilder') as CMB:
        after_saving_contact(sender=Contact,
                             instance=instance,
                             created=True,
                             raw=False)

    assert CMB.mock_calls == [
        mock.call(Configuration(pk=1)),
        mock.call().get_email(instance),
    ]


def test_after_saving_contact_commit(transactional_db):
    call_command('loaddata', 'chloroform/tests/test_apps.yaml')
    instance = Contact.objects.get(pk=1)
    with mock.patch('chloroform.mails.ChloroformMailBuilder') as CMB:
        after_saving_contact(sender=Contact,
                             instance=instance,
                             created=True,
                             raw=False)

    assert CMB.mock_calls == [
        mock.call(Configuration(pk=1)),
        mock.call().get_email(instance),
        mock.call().get_email(instance).send(),
    ]
