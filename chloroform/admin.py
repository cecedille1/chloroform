# -*- coding: utf-8 -*-


from django.contrib import admin
from django.conf import settings

from chloroform.models import (
    Configuration,
    Metadata,
    Alternative,
    Requirement,
    Contact,
    ContactMetadata,
)


class AlternativeInline(admin.TabularInline):
    model = Alternative
    fields = [
        'label',
        'value',
    ]


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


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
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
