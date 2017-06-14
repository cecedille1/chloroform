# -*- coding: utf-8 -*-


from django.contrib import admin
from django import forms
from django.template import Template, TemplateSyntaxError
from django.conf import settings
from django.utils.translation import ugettext as _

from chloroform.models import (
    Configuration,
    Metadata,
    Alternative,
    Requirement,
    Contact,
    ContactMetadata,
)

try:
    from djangocms_text_ckeditor.fields import HTMLFormField
except ImportError:
    HTMLFormField = None


class AlternativeInline(admin.TabularInline):
    model = Alternative
    fields = [
        'label',
        'value',
        'order',
    ]


if 'adminsortable2' in settings.INSTALLED_APPS:
    from adminsortable2.admin import SortableInlineAdminMixin
    AlternativeInline = type(AlternativeInline)('AlternativeInline',
                                                (SortableInlineAdminMixin, AlternativeInline),
                                                {})


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = [
        'verbose_name',
        'name',
        'type_display',
    ]
    fields = [
        'verbose_name',
        'name',
        'type',
    ]
    prepopulated_fields = {
        'name': ['verbose_name']
    }

    inlines = [
        AlternativeInline
    ]

    def get_inline_instances(self, request, obj=None):
        if obj is None or obj.type != 'alternative':
            return []
        return super(MetadataAdmin, self).get_inline_instances(request, obj)

    def type_display(self, metadata):
        return metadata.get_type_display()


class RequirementInline(admin.TabularInline):
    model = Requirement
    fields = [
        'metadata',
        'required',
    ]


class ConfigurationForm(forms.ModelForm):
    if HTMLFormField:
        success_message = Configuration._meta.get_field('success_message').formfield(
            widget=None,
            form_class=HTMLFormField,
        )

    class Meta:
        model = Configuration
        fields = [
            'name',
            'target',
            'success_message',
            'subject',
        ]

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        try:
            Template(subject)
        except TemplateSyntaxError:
            raise forms.ValidationError(_('Incorrect template syntax'))
        return subject


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    form = ConfigurationForm
    list_display = [
        'name',
    ]
    inlines = [
        RequirementInline,
    ]


class ContactMetadataInline(admin.TabularInline):
    model = ContactMetadata
    fields = [
        'name',
        'value',
    ]
    readonly_fields = [
        'name',
    ]


class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = [
        'email',
        'creation_date',
        'configuration',
    ]
    list_filters = [
        'configuration',
    ]
    fields = [
        'email',
        'message',
    ]
    inlines = [
        ContactMetadataInline
    ]


if 'import_export' in settings.INSTALLED_APPS:
    from import_export.admin import ExportMixin
    from chloroform.resources import ContactResource
    metaclass = type(ContactAdmin)
    ContactAdmin = metaclass('ContactAdmin', (ExportMixin, ContactAdmin), {
        'resource_class': ContactResource,
    })


admin.site.register(Contact, ContactAdmin)
