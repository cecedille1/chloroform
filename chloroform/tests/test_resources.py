# -*- coding: utf-8 -*-
import pytest
import datetime

from django.utils.timezone import utc

from chloroform.models import Contact
from chloroform.factories import (
    ConfigurationFactory,
    ContactFactory,
    RequirementFactory,
    ContactMetadataFactory,
)
from chloroform.resources import ContactResource


@pytest.mark.django_db
def test_export_headers_empty():
    cr = ContactResource()
    export = cr.export()
    assert export.headers == ['creation_date', 'email']


@pytest.mark.django_db
def test_export_headers():
    c = ConfigurationFactory(metadatas=[])
    RequirementFactory(configuration=c, metadata__verbose_name='abc', order=1)
    RequirementFactory(configuration=c, metadata__verbose_name='def', order=2)

    ContactFactory(configuration=c)

    cr = ContactResource()
    export = cr.export()
    assert export.headers == ['creation_date', 'email', 'abc', 'def']


@pytest.mark.django_db
def test_export_headers_multiconf():
    c1 = ConfigurationFactory(metadatas=[])
    RequirementFactory(configuration=c1, metadata__verbose_name='abc', order=1)
    ContactFactory(configuration=c1)

    c2 = ConfigurationFactory(metadatas=[])
    RequirementFactory(configuration=c2, metadata__verbose_name='def', order=2)
    ContactFactory(configuration=c2)

    cr = ContactResource()
    export = cr.export()
    assert export.headers == ['creation_date', 'email', 'abc', 'def']


@pytest.fixture
def alter_auto_now():
    Contact._meta.get_field('creation_date').auto_now_add = False
    yield
    Contact._meta.get_field('creation_date').auto_now_add = True


@pytest.mark.django_db
@pytest.mark.usefixtures('alter_auto_now')
def test_export():
    c = ConfigurationFactory(metadatas=[])
    RequirementFactory(configuration=c, metadata__verbose_name='abc', order=1)
    RequirementFactory(configuration=c, metadata__verbose_name='def', order=2)

    ContactFactory(configuration=c,
                   email='abc@ghi.com',
                   creation_date=datetime.datetime(
                       2016, 6, 15, 5, 9, tzinfo=utc,
                   ))

    cr = ContactResource()
    export = cr.export()
    assert export.headers == ['creation_date', 'email', 'abc', 'def']
    assert list(export) == [('2016-06-15 05:09:00', 'abc@ghi.com', '', '')]


@pytest.mark.django_db
@pytest.mark.usefixtures('alter_auto_now')
def test_export_metadata():
    c = ConfigurationFactory(metadatas=[])
    RequirementFactory(configuration=c,
                       metadata__name='abc',
                       metadata__verbose_name='abc',
                       order=1)
    RequirementFactory(configuration=c,
                       metadata__name='def',
                       metadata__verbose_name='def',
                       order=2)

    ct = ContactFactory(configuration=c, email='abc@ghi.com',
                        creation_date=datetime.datetime(2016, 6, 15, 5, 9, tzinfo=utc,))
    ContactMetadataFactory(contact=ct, name='abc', value=1)
    ContactMetadataFactory(contact=ct, name='def', value='jjj')

    cr = ContactResource()
    export = cr.export()
    assert list(export) == [('2016-06-15 05:09:00', 'abc@ghi.com', '1', 'jjj')]


@pytest.mark.django_db
@pytest.mark.usefixtures('alter_auto_now')
def test_export_metadata_multiconf():
    c1 = ConfigurationFactory(metadatas=[])
    RequirementFactory(configuration=c1, metadata__name='abc',
                       metadata__verbose_name='abc', order=1)
    ct1 = ContactFactory(configuration=c1, email='abc@ghi.com',
                         creation_date=datetime.datetime(2016, 6, 15, 5, 9, tzinfo=utc,))
    ContactMetadataFactory(contact=ct1, name='abc', value=1)

    c2 = ConfigurationFactory(metadatas=[])
    RequirementFactory(configuration=c2, metadata__name='def',
                       metadata__verbose_name='def', order=2)
    ct2 = ContactFactory(configuration=c2, email='klm@ghi.com',
                         creation_date=datetime.datetime(2016, 6, 15, 5, 10, tzinfo=utc,))
    ContactMetadataFactory(contact=ct2, name='def', value='jjj')

    cr = ContactResource()
    export = cr.export()
    assert list(export) == [('2016-06-15 05:09:00', 'abc@ghi.com', '1', ''),
                            ('2016-06-15 05:10:00', 'klm@ghi.com', '', 'jjj')]
