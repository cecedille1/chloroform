# -*- coding: utf-8 -*-

from django import forms
from django.db import transaction

from chloroform.models import Contact, ContactMetadata


class BaseForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'email',
            'message',
        ]

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
        fields = {}
        for req in self.requirements:
            fields[req.metadata.name] = req.get_field()
        metacls = type(BaseForm)
        return metacls('ContactForm', (BaseForm, ), fields)
