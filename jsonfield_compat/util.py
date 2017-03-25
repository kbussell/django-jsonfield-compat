from __future__ import print_function

from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.db import connection


def is_db_postgresql():
    return connection.vendor == 'postgresql'


def django_supports_native_jsonfield():
    return (DJANGO_VERSION[0] == 1 and DJANGO_VERSION[1] >= 9) or DJANGO_VERSION[0] > 1


def use_native_jsonfield():
    return django_supports_native_jsonfield() and is_db_postgresql() and \
        getattr(settings, 'USE_NATIVE_JSONFIELD', False)
