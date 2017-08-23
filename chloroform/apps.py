# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ChloroformAppConfig(AppConfig):
    name = 'chloroform'
    verbose_name = _('Chloroform Contact form builder')

    def ready(self):
        import chloroform.checks  # noqa
