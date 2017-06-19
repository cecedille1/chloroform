# -*- coding: utf-8 -*-

import importlib

from django.dispatch import receiver
from django.conf import settings
from django.test.signals import setting_changed
from django.core.exceptions import ImproperlyConfigured

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


_form_helper_module = uninitialized = object()


class ChloroformHelper(FormHelper):
    def __init__(self, *args, **kw):
        super(ChloroformHelper, self).__init__(*args, **kw)
        self.add_input(Submit('submit', _('Submit')))


class ChloroformTagHelper(ChloroformHelper):
    pass


@receiver(setting_changed)
def on_setting_changed(sender, setting, **kw):
    global _form_helper_module
    if setting == 'CHLOROFORM_HELPERS_MODULE':
        _form_helper_module = uninitialized


def get_form_helper_module():
    global _form_helper_module
    if _form_helper_module is uninitialized:
        module_name = getattr(settings, 'CHLOROFORM_HELPERS_MODULE', None)
        if module_name is not None:
            _form_helper_module = importlib.import_module(module_name)
    return _form_helper_module


class FormHelperGetterMixin(object):
    form_helper_class = None

    def get_form_helper_class(self):
        if self.form_helper_class is None:
            raise ImproperlyConfigured(u'Missing form_helper_class attribute on class {}'.format(self.__class__))

        module = get_form_helper_module()
        try:
            return getattr(module, self.form_helper_class.__name__)
        except AttributeError:
            pass
        return self.form_helper_class

    def get_form_helper(self, form=None):
        helper_class = self.get_form_helper_class()
        kwargs = self.get_form_helper_kwargs()
        kwargs.setdefault('form', form)
        return helper_class(**kwargs)

    def get_form_helper_kwargs(self):
        return {}


class FormHelperMixin(FormHelperGetterMixin):
    def get_context_data(self, **kw):
        context = super(FormHelperMixin, self).get_context_data(**kw)
        form = context.get('form')
        context.update({
            'form_helper': self.get_form_helper(form),
        })
        return context
