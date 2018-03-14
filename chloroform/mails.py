# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template
from django.template import Template, Context
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text


class ChloroformMailBuilder(object):
    body_template = 'chloroform/mails/notification.txt'
    body_html_template = 'chloroform/mails/notification.html'

    def __init__(self, configuration, domain=None, request=None):
        self.configuration = configuration
        self.to_email_addresses = configuration.get_targets()
        self.subject_template = Template(force_text(configuration.subject))

        body_template = 'chloroform/mails/notification_{}.txt'.format(configuration.name)
        self.body_template = select_template([body_template, self.__class__.body_template])

        body_html_template = 'chloroform/mails/notification_{}.html'.format(configuration.name)
        self.body_html_template = select_template([body_html_template, self.__class__.body_html_template])

        if domain is None and request:
            domain = request.build_absolute_uri('/').rstrip('/')
        else:
            domain = getattr(settings, 'CHLOROFORM_DOMAIN', None)
        if domain is None:
            raise ImproperlyConfigured('Chloroform needs to know the domain'
                                       ' with the setting CHLOROFORM_DOMAIN or with the request')
        self.domain = domain

    def get_context(self, contact):
        return {
            'contact': contact,
            'domain': self.domain,
            'site': self.domain,
            'metadata': {
                name: value
                for name, value in contact.metadatas.values_list('name', 'value')
            },
        }

    def get_email(self, contact):
        if contact.configuration_id != self.configuration.pk:
            raise ValueError('Mismatching configuration')
        context = self.get_context(contact)
        message = EmailMultiAlternatives(
            self.subject_template.render(Context(context)).strip().replace('\n', ' '),
            self.body_template.render(context),
            self.get_from_email_address(contact),
            self.get_to_email_addresses(contact),
        )
        message.attach_alternative(self.body_html_template.render(context), 'text/html')
        return message

    def get_from_email_address(self, contact):
        return getattr(settings, 'CHLOROFORM_FROM_EMAIL', None) or settings.DEFAULT_FROM_EMAIL

    def get_to_email_addresses(self, context):
        if self.to_email_addresses:
            return self.to_email_addresses
        return getattr(settings, 'CHLOROFORM_TARGET_EMAILS', None) or []
