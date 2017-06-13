# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.core.checks import Error, register


@register()
def check_settings(app_configs, **kwargs):
    from django.conf import settings
    errors = []
    if hasattr(settings, 'CHLOROFORM_DOMAIN'):
        parsed = urlparse(settings.CHLOROFORM_DOMAIN)
        if not parsed.scheme or parsed.path:
            errors.append(Error(
                'setting CHLOROFORM_DOMAIN must be an URL with a scheme and without a path',
                id='chloroform.E0001',
            ))
    return errors
