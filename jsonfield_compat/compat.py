import json
import six
from functools import partial

try:
    from django.contrib.postgres.fields import JSONField as NativeJSONField
except ImportError:  # pragma: no cover
    # If using Django 1.8, don't worry about trying to be correct.
    # We won't be using the native field.
    NativeJSONField = object

from django.conf import settings
from django.utils.module_loading import import_string
from psycopg2.extras import Json


def _get_jsonfield_encoder_class():
    encoder_class = getattr(settings, 'JSONFIELD_ENCODER_CLASS', None)
    if encoder_class:
        if isinstance(encoder_class, six.string_types):
            encoder_class = import_string(encoder_class)

        return encoder_class


def _get_dumps():
    return partial(json.dumps, cls=_get_jsonfield_encoder_class())


class _JSONField(NativeJSONField):
    """ Patches Django's JSONField to use django-jsonfield's
        JSONFIELD_ENCODER_CLASS setting
    """
    def get_prep_value(self, value):
        if value is not None:
            return Json(value, dumps=_get_dumps())
        return value

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('has_key', 'has_keys', 'has_any_keys'):
            return value
        if isinstance(value, (dict, list)):
            return Json(value, dumps=_get_dumps())
        return super(_JSONField, self).get_prep_lookup(lookup_type, value)

    def deconstruct(self):
        name, _, args, kwargs = super(_JSONField, self).deconstruct()
        kwargs.setdefault('default', dict)
        path = 'jsonfield_compat.fields.JSONField'
        return name, path, args, kwargs
