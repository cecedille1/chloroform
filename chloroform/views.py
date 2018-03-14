# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.utils.translation import ugettext as _
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

try:
    from django.db.transaction import on_commit
except ImportError:
    def on_commit(fn):
        fn()

from chloroform.helpers import ChloroformHelper, FormHelperMixin
from chloroform.forms import ContactFormBuilder
from chloroform.mails import ChloroformMailBuilder
from chloroform.models import (
    Configuration,
)


class ChloroformView(SingleObjectMixin, FormHelperMixin, FormView):
    queryset = Configuration.objects.all()
    slug_field = 'name'
    slug_url_kwarg = 'configuration'
    template_name = 'chloroform/form.html'
    context_object_name = 'configuration'
    form_helper_class = ChloroformHelper

    def get_form_class(self):
        fb = ContactFormBuilder(self.object)
        return fb.get_form()

    def get_form_helper(self, form=None):
        helper = super(ChloroformView, self).get_form_helper(form)
        if self.slug_url_kwarg not in self.kwargs:
            helper.form_action = reverse('default-chloroform')
        else:
            helper.form_action = reverse('chloroform', args=[self.object.name])

        all_fields = set(form.fields)
        required_fields = {name for name, f in form.fields.items() if f.required}
        declared_fields = {name for pos, name in helper.layout.get_field_names()}

        if not required_fields.issubset(declared_fields):
            raise ImproperlyConfigured(_('Not all required fields are declared in the form helper: {}').format(
                required_fields.difference(declared_fields),
            ))
        if not declared_fields.issubset(all_fields):
            raise ImproperlyConfigured(_('There are extra fields in the form helper: {}').format(
                ', '.join(declared_fields.difference(all_fields)),
            ))
        return helper

    def get_object(self):
        if self.slug_url_kwarg in self.kwargs:
            return super(ChloroformView, self).get_object()

        qs = self.get_queryset()
        try:
            return qs.get_default()
        except Configuration.DoesNotExist:
            return Configuration(name='default')

    def get(self, request, *args, **kw):
        self.object = self.get_object()
        return super(ChloroformView, self).get(request, *args, **kw)

    def post(self, request, *args, **kw):
        self.object = self.get_object()
        return super(ChloroformView, self).post(request, *args, **kw)

    def form_valid(self, form):
        if not self.object.pk:
            self.object.save()
        form.instance.configuration = self.object
        instance = form.save()
        self.send_email(instance)
        return super(ChloroformView, self).form_valid(form)

    def get_success_url(self):
        if self.slug_url_kwarg not in self.kwargs:
            return reverse('default-chloroform-success')
        return reverse('chloroform-success', args=[self.object.name])

    def send_email(self, contact):
        cmb = ChloroformMailBuilder(self.object)
        email = cmb.get_email(contact)

        @on_commit
        def send_email():
            email.send()


class ChloroformSuccessView(DetailView):
    queryset = Configuration.objects.all()
    slug_field = 'name'
    slug_url_kwarg = 'configuration'
    template_name = 'chloroform/success.html'
    context_object_name = 'configuration'

    def get_object(self):
        if self.slug_url_kwarg in self.kwargs:
            return super(ChloroformSuccessView, self).get_object()
        try:
            return self.get_queryset().get_default()
        except Configuration.DoesNotExist:
            return Configuration(
                success_message=_('Thank you for contacting us.'),
            )
