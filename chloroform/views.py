# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from chloroform.helpers import ChloroformHelper, FormHelperMixin
from chloroform.forms import ContactFormBuilder
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
        form.save()
        return super(ChloroformView, self).form_valid(form)

    def get_success_url(self):
        if self.slug_url_kwarg not in self.kwargs:
            return reverse('default-chloroform-success')
        return reverse('chloroform-success', args=[self.object.name])


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
