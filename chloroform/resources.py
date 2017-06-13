# -*- coding: utf-8 -*-

from import_export import resources, fields

from chloroform.models import Contact, Metadata


class MetadataField(fields.Field):
    def get_value(self, instance):
        for m in instance.metadatas.all():
            if m.name == self.attribute:
                return m.value


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = [
            'creation_date',
            'email',
        ]

    def before_export(self, queryset, *args, **kw):
        meta_data = Metadata.objects.filter(
            requirement__configuration__in=queryset.values('configuration'),
        )
        self.fields.update([
            (m.name, MetadataField(
                attribute=m.name,
                column_name=m.verbose_name
            ))
            for m in meta_data
        ])

    def get_queryset(self):
        return super(ContactResource, self).get_queryset().prefetch_related('metadatas')

    def export(self, queryset=None, *args, **kw):
        if queryset is not None:
            queryset = queryset.prefetch_related('metadatas')
        return super(ContactResource, self).export(queryset, *args, **kw)
