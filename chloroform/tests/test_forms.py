# -*- coding: utf-8 -*-

import pytest
import os

from chloroform.forms import ContactFormBuilder, BaseForm
from chloroform.models import Configuration
from django.core.management import call_command


@pytest.fixture
def disable_recatpcha():
    os.environ['RECAPTCHA_TESTING'] = 'True'
    yield
    del os.environ['RECAPTCHA_TESTING']


@pytest.mark.usefixtures('disable_recatpcha', 'db')
def test_form_base_recaptcha(settings):
    if 'captcha' not in settings.INSTALLED_APPS:
        pytest.skip('This test requires django-recaptcha')

    bf = BaseForm({
        'message': 'oh romeo',
        'email': 'julliet@shakespeare.org',
        'g-recaptcha-response': 'PASSED',
        'recaptcha_response_field': 'PASSED',
    })
    assert bf.is_valid(), bf.errors
    assert bf.cleaned_data == {
        'message': 'oh romeo',
        'email': 'julliet@shakespeare.org',
    }


@pytest.mark.usefixtures('db')
def test_form_base():
    bf = BaseForm({
        'message': 'oh romeo',
        'email': 'julliet@shakespeare.org',
    })
    assert bf.is_valid(), bf.errors

    bf.instance.configuration = Configuration.objects.create()
    instance = bf.save()
    assert instance.email == 'julliet@shakespeare.org'
    assert instance.message == 'oh romeo'


@pytest.fixture
@pytest.mark.usefixtures('db')
def configuration():
    call_command('loaddata', 'chloroform/tests/test_forms.yaml')
    return Configuration.objects.get(pk=1)


@pytest.fixture
def fb(configuration):
    return ContactFormBuilder(configuration)


@pytest.mark.usefixtures('db')
def test_form_built(fb, configuration):
    form_class = fb.get_form()
    form = form_class({
        'message': 'oh romeo',
        'email': 'julliet@shakespeare.org',
        'prenom': 'Julliet',
        'nom': 'Capulet',
        'birthdate': '1544-06-11',
    })
    assert form.is_valid()
    form.instance.configuration = configuration
    instance = form.save()

    assert dict(instance.metadatas.values_list('name', 'value')) == {
        'nom': 'Capulet',
        'prenom': 'Julliet',
    }


@pytest.mark.usefixtures('db')
def test_form_built(fb):
    form_class = fb.get_form()
    assert list(form_class().fields) == [
        'email',
        'message',
        'prenom',
        'nom',
    ]
