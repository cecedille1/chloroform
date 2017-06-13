# -*- coding: utf-8 -*-

import pytest

from django.template import Template, Context

from chloroform.models import Configuration


@pytest.mark.django_db
def test_chloroform_ttag():
    Configuration.objects.create(name='default')
    t = Template('{% load chloroform %}{% chloroform %}')
    rendered = t.render(Context())
    assert 'form' in rendered
    assert 'chloroform-default' in rendered


@pytest.mark.django_db
def test_chloroform_ttag_alternative():
    Configuration.objects.create(name='alternative')
    t = Template('{% load chloroform %}{% chloroform "alternative" %}')
    rendered = t.render(Context())
    assert 'form' in rendered
    assert 'chloroform-alternative' in rendered
