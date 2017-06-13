# -*- coding: utf-8 -*-


import pytest

from django.core.management import call_command
from django import forms

from chloroform.models import (
    Configuration,
    Metadata,
)


@pytest.mark.django_db
def test_configuration_get_default():
    call_command('loaddata', 'chloroform/tests/test_models.yaml')
    c = Configuration.objects.get_default()
    assert c.pk == 1


@pytest.mark.django_db
def test_configuration_get_target():
    call_command('loaddata', 'chloroform/tests/test_models.yaml')
    c = Configuration.objects.get(pk=1)
    assert c.get_targets() == ['chloroform@emencia.com', 'chloroform@emencia.io']

    c = Configuration.objects.get(pk=2)
    assert c.get_targets() == []


def test_metadata_get_field_class():
    m = Metadata(type='bool')
    assert m.get_field_class() == forms.BooleanField
    m = Metadata(type='phone')
    assert m.get_field_class() == forms.CharField


def test_metadata_get_field_kwargs():
    m = Metadata(type='bool',
                 verbose_name='abc',
                 description='def')
    assert m.get_field_kwargs() == {
        'label': 'abc',
        'help_text': 'def',
    }

    m = Metadata(type='phone')
    assert m.get_field_class() == forms.CharField
    assert m.get_field_kwargs() == {
        'label': '',
        'help_text': '',
    }
