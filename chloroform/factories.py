# -*- coding: utf-8 -*-

import factory
import factory.django
from django.utils.timezone import utc

from chloroform.models import (
    Alternative,
    Configuration,
    Contact,
    ContactMetadata,
    Metadata,
    Requirement,
)


class ConfigurationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('word')
    target = factory.Faker('email')
    success_message = factory.Faker('paragraph')
    subject = factory.Faker('sentence')

    @factory.post_generation
    def metadatas(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted is not None:
            if extracted == []:
                return
        assert not extracted and not kwargs
        RequirementFactory.create_batch(4, configuration=self)

    class Params:
        is_default = factory.Trait(
            name='default',
        )

    class Meta:
        model = Configuration


class MetadataFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('word')
    verbose_name = factory.Faker('word')
    description = factory.Maybe(factory.Faker('paragraph'))
    type = factory.Faker('random_element', elements=[
            'name',
            'address'
            'email',
            'text',
    ])

    @factory.post_generation
    def alternatives(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted is not None:
            if extracted == []:
                return
        assert not extracted and not kwargs
        AlternativeFactory.create_batch(4, metadata=self)

    class Meta:
        model = Metadata


class AlternativeFactory(factory.django.DjangoModelFactory):
    metadata = factory.SubFactory(MetadataFactory)
    label = factory.Faker('word')
    value = factory.Faker('word')
    order = factory.Sequence(int)

    class Meta:
        model = Alternative


class RequirementFactory(factory.django.DjangoModelFactory):
    metadata = factory.SubFactory(MetadataFactory)
    configuration = factory.SubFactory(ConfigurationFactory)
    required = factory.Faker('boolean')
    order = factory.Sequence(int)

    class Meta:
        model = Requirement


class ContactFactory(factory.django.DjangoModelFactory):
    configuration = factory.SubFactory(ConfigurationFactory)
    creation_date = factory.Faker('past_datetime', tzinfo=utc)
    email = factory.Faker('email')
    message = factory.Faker('paragraph')

    class Meta:
        model = Contact


class ContactMetadataFactory(factory.django.DjangoModelFactory):
    contact = factory.SubFactory(ConfigurationFactory)
    name = factory.Faker('word')
    value = factory.Faker('word')

    class Meta:
        model = ContactMetadata
