# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django import forms
from django.forms import widgets


class ConfigurationQuerySet(models.QuerySet):
    def get_default(self):
        return self.get(name='default')


@python_2_unicode_compatible
class Configuration(models.Model):
    objects = ConfigurationQuerySet.as_manager()

    name = models.SlugField(
        default='default',
        unique=True,
        max_length=255,
    )
    target = models.CharField(
        _('Recipient of mails sent with this configuration'),
        blank=True,
        max_length=2000,
        help_text=_('An email or a list of emails separated by ;')
    )
    success_message = models.TextField(
        _('Success message'),
        help_text=_('This message is shown to the user after he/she uses the contact form'),
        blank=True,
    )
    subject = models.CharField(
        _('Subject'),
        help_text=_('Subject of the mail sent to the target'),
        max_length=1000,
        default=_('Contact on {{site}}'),
    )
    metadatas = models.ManyToManyField(
        'Metadata',
        through='Requirement',
    )

    def get_targets(self):
        if not self.target:
            return []
        return self.target.split(';')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Metadata(models.Model):
    name = models.SlugField(
        _('Name of the field in the HTML'),
        max_length=255,
    )
    verbose_name = models.CharField(
        _('Name shown to the user'),
        max_length=255,
    )
    description = models.TextField(
        _('Description or help text shown to the user'),
        blank=True,
    )
    type = models.CharField(
        _('Type of metadata, set the validation and the HTML field'),
        max_length=100,
        choices=[
            ('name', _('Name')),
            ('phone', _('Phone')),
            ('address', _('Address')),
            ('email', _('Email')),
            ('bool', _('Boolean')),
            ('text', _('Text')),
            ('message', _('Message')),
            ('alternative', _('Choice')),
        ]
    )

    def __str__(self):
        return self.verbose_name

    def get_field_class(self):
        mapping = {
            'email': forms.EmailField,
            'bool': forms.BooleanField,
            'alternative': forms.ModelChoiceField,
        }
        return mapping.get(self.type, forms.CharField)

    def get_field_kwargs(self):
        kwargs = {
            'label': self.verbose_name,
            'help_text': self.description,
        }
        if self.type in {'address', 'text', 'message'}:
            kwargs['widget'] = widgets.Textarea()
        elif self.type in {'alternative'}:
            kwargs['queryset'] = self.alternatives.all()

        return kwargs


@python_2_unicode_compatible
class Alternative(models.Model):
    metadata = models.ForeignKey(
        Metadata,
        related_name='alternatives',
    )
    label = models.CharField(
        max_length=1000,
    )
    value = models.CharField(
        max_length=255,
        blank=True
    )
    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = [
            'order',
        ]

    def get_value(self):
        return self.value or self.label

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Requirement(models.Model):
    metadata = models.ForeignKey(
        Metadata,
    )
    configuration = models.ForeignKey(
        Configuration,
        related_name='requirements',
    )
    required = models.BooleanField(
        default=False,
    )

    class Meta:
        unique_together = [
            ('metadata', 'configuration'),
        ]

    def __str__(self):
        return u'{} on {}'.format(self.metadata, self.configuration)

    def get_field(self):
        field_class = self.metadata.get_field_class()
        field_kwargs = self.metadata.get_field_kwargs()
        field_kwargs['required'] = self.required
        return field_class(**field_kwargs)


@python_2_unicode_compatible
class Contact(models.Model):
    configuration = models.ForeignKey(
        Configuration,
    )
    creation_date = models.DateTimeField(
        _('Creation date'),
        auto_now_add=True,
    )
    email = models.EmailField(
        _('Email'),
    )
    message = models.TextField(
        _('Message'),
    )

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.email


@python_2_unicode_compatible
class ContactMetadata(models.Model):
    contact = models.ForeignKey(
        Contact,
        related_name='metadatas',
    )
    name = models.CharField(
        max_length=255,
    )
    value = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.value
