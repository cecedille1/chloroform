# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

try:
    from django.db.transaction import on_commit
except ImportError:
    def on_commit(fn):
        fn()


class ChloroformAppConfig(AppConfig):
    name = 'chloroform'
    verbose_name = _('Chloroform Contact form builder')

    def ready(self):
        Contact = self.get_model('Contact')
        # registering signals with the model's string label
        post_save.connect(after_saving_contact, sender=Contact)

        import chloroform.checks  # noqa


def after_saving_contact(sender, instance, created, raw, **kw):
    if not created or raw:
        return

    from chloroform.mails import ChloroformMailBuilder
    cmb = ChloroformMailBuilder(instance.configuration)
    email = cmb.get_email(instance)

    @on_commit
    def send_email():
        email.send()
