import sys
import unittest
from decimal import Decimal

from django.conf import settings
from django.db import connection
from django.test import TestCase

from jsonfield_compat.util import is_db_postgresql
from test_app.models import MyModel


@unittest.skipUnless(
    is_db_postgresql() and getattr(settings, 'TEST_CREATE_DATA_AS_TEXT', False),
    "only relevant if postgresql and using native JSONField")
class JSONFieldCompatTest(TestCase):
    def test_native_jsonfield_uses_encoder(self):
        data = {'name': 'amount', 'value': Decimal('199.99')}

        # Create will fail trying to serialize a Decimal if the encoder isn't used
        m = MyModel.objects.create(data=data)

        m.refresh_from_db()
        expected = {'name': 'amount', 'value': '199.99'}
        self.assertEqual(m.data, expected)

        m2 = MyModel.objects.get(data=expected)
        self.assertEqual(m, m2)

        m3 = MyModel.objects.get(data__has_key='name')
        self.assertEqual(m, m3)

    def test_data_is_none(self):
        m = MyModel.objects.create(data=None)
        m2 = MyModel.objects.get(data=None)
        self.assertEqual(m, m2)

    def test_db_column_converted_to_json(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "select data_type from information_schema.columns "
                "where table_name = 'test_app_mymodel' "
                "  and column_name = 'data';")
            self.assertEqual(cursor.fetchone()[0], 'jsonb')


class ZZZJSONFieldCompatImportTest(TestCase):
    """ This test case needs to run last. It ends up importing jsonfield, which changes
        how psycopg2 works.
    """
    def tearDown(self):
        # Unload modules between tests so JSONField and JSONFormField don't get cached
        keys = list(filter(lambda m: m.startswith('jsonfield'), sys.modules.keys()))
        for key in keys:
            sys.modules.pop(key)

    def test_use_native_jsonfield(self):
        from jsonfield_compat.util import is_db_postgresql, use_native_jsonfield

        self.assertEqual(use_native_jsonfield(), is_db_postgresql())

        with self.settings(USE_NATIVE_JSONFIELD=False):
            self.assertFalse(use_native_jsonfield())

    def test_right_model_field_used(self):
        from jsonfield_compat.util import is_db_postgresql

        if is_db_postgresql():
            from jsonfield_compat import JSONField
            from jsonfield_compat.compat import _JSONField
            self.assertTrue(JSONField is _JSONField)
        else:
            from jsonfield_compat import JSONField
            from jsonfield.fields import JSONField as _JSONField
            self.assertTrue(JSONField is _JSONField)

    def test_right_form_field_used(self):
        from jsonfield_compat.util import is_db_postgresql

        if is_db_postgresql():
            from jsonfield_compat.forms import JSONFormField
            from django.contrib.postgres.fields import JSONField as _JSONFormField
            self.assertTrue(JSONFormField is _JSONFormField)
        else:
            from jsonfield_compat.forms import JSONFormField
            from jsonfield.forms import JSONFormField as _JSONFormField
            self.assertTrue(JSONFormField is _JSONFormField)

    def test_use_jsonfield_model_field(self):
        with self.settings(USE_NATIVE_JSONFIELD=False):
            from jsonfield_compat import JSONField
            from jsonfield.fields import JSONField as _JSONField
            self.assertTrue(JSONField is _JSONField)

    def test_use_jsonfield_form_field(self):
        with self.settings(USE_NATIVE_JSONFIELD=False):
            from jsonfield_compat.forms import JSONFormField
            from jsonfield.forms import JSONFormField as _JSONFormField
            self.assertTrue(JSONFormField is _JSONFormField)
