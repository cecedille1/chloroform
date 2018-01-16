# -*- coding: utf-8 -*-

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
        for f in BaseForm.Meta.fields:
            # Remove declared fields on the base model
            self.cleaned_data.pop(f, None)
        for k, v in self.cleaned_data.items():
            ContactMetadata.objects.create(contact=contact,
                                           name=k,
                                           value=v)
        return contact


class ContactFormBuilder(object):
    def __init__(self, configuration):
        self.configuration = configuration

    @property
    def requirements(self):
        return self.configuration.requirements.select_related('metadata')

    def get_form(self):
        fields = list(BaseForm.Meta.fields)

        attrs = {}
        for req in self.requirements:
            fields.append(req.metadata.name)
            attrs[req.metadata.name] = req.get_field()

        attrs['Meta'] = type('Meta', (BaseForm.Meta, ), {
            'fields': fields
        })
        metacls = type(BaseForm)
        return metacls('ContactForm', (BaseForm, ), attrs)
