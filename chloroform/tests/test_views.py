# -*- coding: utf-8 -*-

import pytest

from django.core.management import call_command
from django.conf.urls import include, url

from chloroform.models import Contact
from chloroform.views import ChloroformView, ChloroformSuccessView


urlpatterns = [
    url('^', include('chloroform.urls')),
]


@pytest.mark.django_db
def test_chloroform_view(rf):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')

    cfv = ChloroformView.as_view()
    request = rf.get('/')
    resp = cfv(request)

    assert resp.status_code == 200
    assert set(resp.context_data['form'].fields) == {'email', 'message', 'prenom', 'nom'}
    assert b'mark01' in resp.render().content


@pytest.mark.django_db
def test_chloroform_view_none(rf):
    cfv = ChloroformView.as_view()
    request = rf.get('/')
    resp = cfv(request)

    assert resp.status_code == 200
    assert set(resp.context_data['form'].fields) == {'email', 'message'}


@pytest.mark.django_db
def test_chloroform_view_alternative(rf):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    cfv = ChloroformView.as_view()
    request = rf.get('/')
    resp = cfv(request, configuration='alternative')

    assert resp.status_code == 200
    assert set(resp.context_data['form'].fields) == {'email', 'message', 'optin'}
    assert b'mark03' in resp.render().content


@pytest.mark.django_db
@pytest.mark.urls('chloroform.tests.test_views')
def test_chloroform_fill_alternative(rf):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    cfv = ChloroformView.as_view()
    request = rf.post('/', {
        'email': 'abc@def.org',
        'message': 'blabla',
    })
    resp = cfv(request, configuration='alternative')

    assert resp.status_code == 302
    assert resp['Location'] == '/alternative/success/'

    c = Contact.objects.get()
    assert c.configuration_id == 2
    assert c.email == 'abc@def.org'
    assert c.message == 'blabla'


@pytest.mark.django_db
@pytest.mark.urls('chloroform.tests.test_views')
def test_chloroform_fill_none(rf):
    cfv = ChloroformView.as_view()
    request = rf.post('/', {
        'email': 'abc@def.org',
        'message': 'blabla',
    })
    resp = cfv(request)

    assert resp.status_code == 302
    assert resp['Location'] == '/success/'

    c = Contact.objects.get()
    assert c.configuration_id == 2
    assert c.email == 'abc@def.org'
    assert c.message == 'blabla'


@pytest.mark.django_db
@pytest.mark.urls('chloroform.tests.test_views')
def test_chloroform_fill(rf):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    cfv = ChloroformView.as_view()
    request = rf.post('/', {
        'email': 'abc@def.org',
        'message': 'blabla',
        'prenom': 'John',
        'nom': 'McEnroe',
    })
    resp = cfv(request)

    assert resp.status_code == 302
    assert resp['Location'] == '/success/'

    c = Contact.objects.get()
    assert c.configuration_id == 1
    assert c.email == 'abc@def.org'
    assert c.message == 'blabla'

    assert set(c.metadatas.values_list('name', 'value')) == {
        ('prenom', 'John'),
        ('nom', 'McEnroe'),
    }


@pytest.mark.django_db
def test_chloroform_success(rf):
    cfsv = ChloroformSuccessView.as_view()
    request = rf.get('/')
    resp = cfsv(request)

    assert resp.status_code == 200
    assert resp.context_data['configuration'].pk is None
    assert resp.context_data['configuration'].success_message


@pytest.mark.django_db
def test_chloroform_success(rf):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    cfsv = ChloroformSuccessView.as_view()
    request = rf.get('/')
    resp = cfsv(request)

    assert resp.status_code == 200
    assert resp.context_data['configuration'].pk == 1


@pytest.mark.django_db
def test_chloroform_success_alternative(rf):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    cfsv = ChloroformSuccessView.as_view()
    request = rf.get('/')
    resp = cfsv(request, configuration='alternative')

    assert resp.status_code == 200
    assert resp.context_data['configuration'].pk == 2
