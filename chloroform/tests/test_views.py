# -*- coding: utf-8 -*-

import pytest

from django.core.management import call_command
from django.conf.urls import include, url

from chloroform.models import Contact
from chloroform.views import ChloroformView, ChloroformSuccessView


urlpatterns = [
    url('^', include('chloroform.urls')),
]


@pytest.fixture
def success_view(rf):
    cfsv = ChloroformSuccessView.as_view()

    def do_success_view(**kw):
        request = rf.get('/')
        return cfsv(request, **kw)
    return do_success_view


@pytest.fixture
def chloro_view(rf):
    cfv = ChloroformView.as_view()

    def inner_chloro_view(**kw):
        request = rf.get('/')
        return cfv(request, **kw)
    return inner_chloro_view


@pytest.fixture
def fill_view(rf):
    cfv = ChloroformView.as_view()

    def inner_chloro_view(data=None, **kw):
        data = data or {
            'email': 'abc@def.org',
            'message': 'blabla',
        }
        request = rf.post('/', data=data)
        return cfv(request, **kw)
    return inner_chloro_view


@pytest.mark.django_db
def test_chloroform_view(chloro_view):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')

    resp = chloro_view()

    assert resp.status_code == 200
    assert set(resp.context_data['form'].fields) == {'email', 'message', 'prenom', 'nom'}
    assert b'mark01' in resp.render().content


@pytest.mark.django_db
def test_chloroform_view_none(chloro_view):
    resp = chloro_view()

    assert resp.status_code == 200
    assert set(resp.context_data['form'].fields) == {'email', 'message'}


@pytest.mark.django_db
def test_chloroform_view_alternative(chloro_view):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    resp = chloro_view(configuration='alternative')

    assert resp.status_code == 200
    assert set(resp.context_data['form'].fields) == {'email', 'message', 'optin'}
    assert b'mark03' in resp.render().content


@pytest.mark.django_db
@pytest.mark.urls('chloroform.tests.test_views')
def test_chloroform_fill_alternative(fill_view):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    resp = fill_view(configuration='alternative')

    assert resp.status_code == 302
    assert resp['Location'] == '/alternative/success/'

    c = Contact.objects.get()
    assert c.configuration_id == 2
    assert c.email == 'abc@def.org'
    assert c.message == 'blabla'


@pytest.mark.django_db
@pytest.mark.urls('chloroform.tests.test_views')
def test_chloroform_fill_none(fill_view):
    resp = fill_view()

    assert resp.status_code == 302
    assert resp['Location'] == '/success/'

    c = Contact.objects.get()
    assert c.configuration_id
    assert c.email == 'abc@def.org'
    assert c.message == 'blabla'


@pytest.mark.django_db
@pytest.mark.urls('chloroform.tests.test_views')
def test_chloroform_fill(fill_view):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    resp = fill_view({
        'email': 'abc@def.org',
        'message': 'blabla',
        'prenom': 'John',
        'nom': 'McEnroe',
    })

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


@pytest.mark.usefixtures('transactional_db')
def test_chloroform_success_send_mail(fill_view, mailoutbox):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')
    fill_view(configuration='alternative')
    assert mailoutbox
    assert mailoutbox[0].to == ['admin@chloro.form']


@pytest.mark.django_db
def test_chloroform_success(success_view):
    resp = success_view()

    assert resp.status_code == 200
    assert resp.context_data['configuration'].pk is None
    assert resp.context_data['configuration'].success_message


@pytest.mark.django_db
def test_chloroform_success_default(success_view):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')

    resp = success_view()

    assert resp.status_code == 200
    assert resp.context_data['configuration'].pk == 1


@pytest.mark.django_db
def test_chloroform_success_alternative(success_view):
    call_command('loaddata', 'chloroform/tests/test_views.yaml')

    resp = success_view(configuration='alternative')

    assert resp.status_code == 200
    assert resp.context_data['configuration'].pk == 2
