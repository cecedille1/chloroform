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

if 'ckeditor' in settings.INSTALLED_APPS:
    from ckeditor.fields import RichTextFormField
else:
    RichTextFormField = None


if 'modeltranslation' in settings.INSTALLED_APPS:
    from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
    BaseModelAdmin = TranslationAdmin
    BaseTabularInline = TranslationTabularInline
else:
    BaseModelAdmin = admin.ModelAdmin
    BaseTabularInline = admin.TabularInline


class AlternativeInline(BaseTabularInline):
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
class MetadataAdmin(BaseModelAdmin):
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
    class Meta:
        model = Configuration
        fields = [
            'name',
            'target',
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
class ConfigurationAdmin(BaseModelAdmin):
    form = ConfigurationForm
    fields = [
        'name',
        'target',
        'subject',
        'success_message',
    ]
    list_display = [
        'name',
    ]
    inlines = [
        RequirementInline,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'success_message':
            kwargs.update(
                widget=None,
                form_class=RichTextFormField,
            )
        return super(ConfigurationAdmin, self).formfield_for_dbfield(db_field, **kwargs)


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
