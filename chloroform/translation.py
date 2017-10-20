# -*- coding: utf-8 -*-


from modeltranslation.translator import register, TranslationOptions
from chloroform.models import Configuration, Metadata, Alternative


@register(Configuration)
class ConfigurationTranslationOptions(TranslationOptions):
    fields = [
        'success_message',
    ]


@register(Metadata)
class MetadataTranslationOptions(TranslationOptions):
    fields = [
        'verbose_name',
        'description',
    ]


@register(Alternative)
class AlternativeTranslationOptions(TranslationOptions):
    fields = [
        'label',
    ]
