# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django import template

from chloroform.forms import ContactFormBuilder
from chloroform.models import Configuration
from chloroform.helpers import ChloroformTagHelper, FormHelperGetterMixin

register = template.Library()


class ChloroformHelperGetter(FormHelperGetterMixin):
    form_helper_class = ChloroformTagHelper


@register.inclusion_tag('chloroform/tag.html')
def chloroform(name=None):
    if isinstance(name, Configuration):
        conf = name
    elif name is None:
        conf = Configuration.objects.get_default()
    else:
        conf = Configuration.objects.get(name=name)

    helper_getter = ChloroformHelperGetter()
    form_builder = ContactFormBuilder(conf)
    form_class = form_builder.get_form()
    form = form_class()
    return {
        'form_helper': helper_getter.get_form_helper(form),
        'configuration': conf,
        'form': form,
    }
