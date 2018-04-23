# -*- coding: utf-8 -*-

from chloroform.checks import check_settings
from django.apps import apps


def test_check_settings_bad(settings):
    settings.CHLOROFORM_DOMAIN = 'https://emencia.com/123'
    errors = check_settings(apps)
    assert errors


def test_check_settings_good(settings):
    settings.CHLOROFORM_DOMAIN = 'https://emencia.com'
    errors = check_settings(apps)
    assert not errors
