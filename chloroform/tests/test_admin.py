# -*- coding: utf-8 -*-

import pytest

from chloroform.admin import ConfigurationForm


@pytest.mark.django_db
def test_configuration_form():
    cf = ConfigurationForm(data={
        'name': 'default',
        'target': '',
        'success_message': 'blabla',
        'subject': '{{ site }}',
    })
    assert cf.is_valid()


@pytest.mark.django_db
def test_configuration_form_bad():
    cf = ConfigurationForm(data={
        'name': 'default',
        'target': '',
        'success_message': 'blabla',
        'subject': '{%  %}',
    })
    assert not cf.is_valid()
