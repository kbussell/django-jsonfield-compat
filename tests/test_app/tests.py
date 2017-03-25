import unittest
from decimal import Decimal

from django.conf import settings
from django.db import connection
from django.test import TestCase

from jsonfield_compat import is_db_postgresql
from test_app.models import MyModel


class JSONFieldCompatTest(TestCase):
    @unittest.skipUnless(
        is_db_postgresql() and getattr(settings, 'TEST_CREATE_DATA_AS_TEXT', False),
        "only relevant if postgresql and using native JSONField")
    def test_native_jsonfield_uses_encoder(self):
        data = {'name': 'amount', 'value': Decimal('199.99')}

        # Create will fail trying to serialize a Decimal if the encoder isn't used
        m = MyModel.objects.create(data=data)

        m.refresh_from_db()
        self.assertEqual(m.data, {'name': 'amount', 'value': '199.99'})

    @unittest.skipUnless(
        is_db_postgresql() and getattr(settings, 'TEST_CREATE_DATA_AS_TEXT', False),
        "only relevant if postgresql and using native JSONField")
    def test_db_column_converted_to_json(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "select data_type from information_schema.columns "
                "where table_name = 'test_app_mymodel' "
                "  and column_name = 'data';")
            self.assertEqual(cursor.fetchone()[0], 'json')



