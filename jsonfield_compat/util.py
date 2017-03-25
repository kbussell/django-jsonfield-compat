from __future__ import print_function

from django.conf import settings
from django.db import connection


def is_db_postgresql():
    return connection.vendor == 'postgresql'


def use_native_jsonfield():
    return is_db_postgresql() and getattr(settings, 'USE_NATIVE_JSONFIELD', False)
