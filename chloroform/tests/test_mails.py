# -*- coding: utf-8 -*-

import pytest

from django.core.management import call_command

from chloroform.mails import ChloroformMailBuilder
from chloroform.models import Contact, Configuration


@pytest.fixture
@pytest.mark.django_db
def cf(settings):
    settings.CHLOROFORM_DOMAIN = 'https://chloroform.emencia.net'
    settings.CHLOROFORM_TARGET_EMAILS = ['chloroform@emencia.net']
    settings.DEFAULT_FROM_EMAIL = 'contact@emencia.net'

    call_command('loaddata', 'chloroform/tests/test_mails.yaml')

    yield Configuration.objects.get_default(), Contact.objects.get(pk=1)


@pytest.mark.django_db
def test_mail_builder(cf):
    conf, contact = cf
    c = ChloroformMailBuilder(conf)
    e = c.get_email(contact)

    assert 'mark02' in e.body
    assert 'https://chloroform.emencia.net' in e.body


@pytest.mark.django_db
def test_mail_builder_request(cf, rf):
    conf, contact = cf
    c = ChloroformMailBuilder(conf, request=rf.get('/',
                                                   SERVER_NAME='chloroform.emencia.org'))
    e = c.get_email(contact)

    assert 'mark02' in e.body
    assert 'http://chloroform.emencia.org' in e.body


@pytest.mark.django_db
def test_mail_builder_alternative_template(cf):
    conf, contact = cf
    conf.name = 'alternative'
    c = ChloroformMailBuilder(conf)
    e = c.get_email(contact)

    assert 'mark01' in e.body
    assert 'https://chloroform.emencia.net' in e.body


@pytest.mark.django_db
def test_mail_builder_to_conf(cf):
    conf, contact = cf
    conf.target = 'chloroform@emencia.net'
    c = ChloroformMailBuilder(conf)
    e = c.get_email(contact)

    assert e.to == ['chloroform@emencia.net']


@pytest.mark.django_db
def test_mail_builder_to_default(cf):
    conf, contact = cf
    c = ChloroformMailBuilder(conf)
    e = c.get_email(contact)

    assert e.to == ['chloroform@emencia.net']


@pytest.mark.django_db
def test_mail_builder_from_default(cf):
    conf, contact = cf
    c = ChloroformMailBuilder(conf)
    e = c.get_email(contact)

    assert e.from_email == 'contact@emencia.net'


@pytest.mark.django_db
def test_mail_builder_from_conf(settings, cf):
    settings.CHLOROFORM_FROM_EMAIL = 'contact@chloroform.net'
    conf, contact = cf
    c = ChloroformMailBuilder(conf)
    e = c.get_email(contact)

    assert e.from_email == 'contact@chloroform.net'


@pytest.mark.django_db
def test_mail_builder_metadata(cf):
    conf, contact = cf
    c = ChloroformMailBuilder(conf)
    context = c.get_context(contact)

    assert context['metadata'] == {
        'nom': 'Albert',
    }
