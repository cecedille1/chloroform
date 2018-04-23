# -*- coding: utf-8 -*-

import collections

from django import forms
from django.db import transaction
from django.conf import settings

from chloroform.models import Contact, ContactMetadata


if 'captcha' in settings.INSTALLED_APPS:
    from captcha.fields import ReCaptchaField
else:
    ReCaptchaField = None


class BaseForm(forms.ModelForm):
    if ReCaptchaField:
        captcha = ReCaptchaField(attrs={'theme': 'clean'})

    class Meta:
        model = Contact
        fields = [
            'email',
            'message',
        ]
        if ReCaptchaField:
            fields.append('captcha')

    @transaction.atomic
    def save(self):
        contact = super(BaseForm, self).save()
        # Remove declared fields on the base model
        base_fields = frozenset(BaseForm.Meta.fields)
        ContactMetadata.objects.bulk_create([ContactMetadata(
            contact=contact,
            name=k,
            value=v
        ) for k, v in self.cleaned_data.items()
            if k not in base_fields
        ])
        return contact


class ContactFormBuilder(object):
    def __init__(self, configuration):
        self.configuration = configuration

    @property
    def requirements(self):
        return self.configuration.requirements.select_related('metadata')

    def get_form(self):
        attrs = collections.OrderedDict()
        for req in reversed(self.requirements):
            attrs[req.metadata.name] = req.get_field()

        fields = list(attrs)
        fields.extend(f for f in reversed(BaseForm.Meta.fields) if f not in attrs)
        fields.reverse()

        attrs['Meta'] = type('Meta', (BaseForm.Meta, object), {
            'fields': fields,
            'configuration': self.configuration,
        })
        metacls = type(BaseForm)
        return metacls('ContactForm', (BaseForm, ), attrs)
