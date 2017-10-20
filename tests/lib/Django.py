# -*- coding: utf-8 -*-

import shutil
import os

from robot.api import logger
from robot.api.deco import keyword

from django.core import mail
from django.core.management import call_command
from django.conf import settings
from django.apps import apps
from django.db.models import Q
from django.db.utils import ProgrammingError


class DjangoListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, django_lib):
        self.django_lib = django_lib

    def close(self):
        if not os.environ.get('ROBOT_REUSE_DB'):
            self.django_lib.teardown_database()
        self.django_lib.teardown_medias()


class Django(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = DjangoListener(self)

    def django(self, *args):
        command = args[0].lower()
        logger.info('Calling django %s %r' % (command, args[1:]))
        call_command(command, *args[1:], interactive=False)

    def empty_mailbox(self):
        mail.outbox = []

    def get_email_sent_to(self, target):
        if not getattr(mail, 'outbox', None):
            raise AssertionError('No mail sent at all')

        for email in mail.outbox:
            if target in email.to:
                return email
        else:
            raise AssertionError('No mail sent to {}'.format(target))

    def loaddata(self, fixture):
        call_command('loaddata', fixture)

    @keyword('Get ${model} by ${field}=${value}')
    def get_object(self, model, field, value):
        model_class = apps.get_model(model)
        try:
            return model_class.objects.get(Q((field, value)))
        except model_class.DoesNotExist:
            raise AssertionError('Instance of {} with {}={} does not exist'.format(
                model_class, field, value))

    @keyword('Set ${field}=${value} of ${model} where ${filter_field}=${filter_value}')
    def set_object(self, field, value, model, filter_field, filter_value):
        model_class = apps.get_model(model)
        count = model_class.objects.filter(Q((filter_field, filter_value))).update(**{field: value})
        logger.info('Updated {} {}'.format(count, model))

    def teardown_medias(self):
        try:
            shutil.rmtree(settings.MEDIA_ROOT)
        except FileNotFoundError:
            pass

    def _root_db_wrapper(self, db):
        from django.db.utils import load_backend
        backend = load_backend(db['ENGINE'])
        db_root = dict(db)
        db_creation_overide = db.get('DATABASE_CREATION', {})
        if 'NAME' not in db_creation_overide:
            db_creation_overide['NAME'] = 'postgres'

        db_root.update(db_creation_overide)
        return backend.DatabaseWrapper(db_root)

    def setup_database(self):
        for alias, db in settings.DATABASES.items():
            if 'postgresql' in db['ENGINE']:
                db_wrapper = self._root_db_wrapper(db)
                try:
                    with db_wrapper.cursor() as cursor:
                        cursor.execute('CREATE DATABASE {} OWNER {}'.format(db['NAME'], db['USER']))
                except ProgrammingError as e:
                    logger.warn(str(e))
            elif 'sqlite3' in db['ENGINE']:
                try:
                    os.makedirs(os.path.dirname(db['NAME']))
                except OSError as e:
                    # Raise unless it's because it already exists
                    if e.errno != 17:
                        raise
        call_command('migrate')
        call_command('sync_translation_fields', interactive=False)

    def teardown_database(self):
        from django.db import connection
        connection.close()

        for db in settings.DATABASES.values():
            if 'postgresql' in db['ENGINE']:
                db_wrapper = self._root_db_wrapper(db)
                with db_wrapper.cursor() as cursor:
                    cursor.execute('DROP DATABASE {}'.format(db['NAME'], db['USER']))
            elif 'sqlite3' in db['ENGINE']:
                logger.info('Remove %s' % db['NAME'])
                try:
                    os.remove(db['NAME'])
                except FileNotFoundError:
                    pass
