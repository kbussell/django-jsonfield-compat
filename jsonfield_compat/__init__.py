from __future__ import print_function

from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate

USE_NATIVE_JSONFIELD = getattr(settings, 'USE_NATIVE_JSONFIELD', False)


def is_db_postgresql():
    return connection.vendor == 'postgresql'


def use_native_jsonfield():
    return is_db_postgresql() and USE_NATIVE_JSONFIELD


def convert_column_to_json(model, column_name):
    if not is_db_postgresql():
        return

    table_name = model._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(
            "select data_type from information_schema.columns "
            "where table_name = %s and column_name = %s;",
            [table_name, column_name])

        current_type = cursor.fetchone()[0].upper()
        expected_type = 'JSON' if use_native_jsonfield() else 'TEXT'

        if current_type != expected_type:
            print("{app}: Converting {col} to use native {type} field".format(
                app=model._meta.app_label, col=column_name, type=expected_type))

            cursor.execute(
                "ALTER TABLE {table} ALTER COLUMN {col} "
                "TYPE {type} USING {col}::{type};".format(
                    table=table_name, col=column_name, type=expected_type
                )
            )


def convert_model_json_fields(model):
    json_fields = [f for f in model._meta.fields if f.__class__ == JSONField]

    for field in json_fields:
        _, column_name = field.get_attname_column()
        convert_column_to_json(model, column_name)


def handler_convert_json_fields(sender, **kwargs):
    for model in list(sender.get_models()):
        convert_model_json_fields(model)


def register_app(app_config):
    post_migrate.connect(handler_convert_json_fields, sender=app_config)


if use_native_jsonfield():
    from jsonfield_compat.compat import _JSONField
    from django.contrib.postgres.fields import JSONField as _JSONFormField
else:
    from jsonfield.fields import JSONField as _JSONField
    from jsonfield.forms import JSONFormField as _JSONFormField

JSONField = _JSONField
JSONFormField = _JSONFormField
