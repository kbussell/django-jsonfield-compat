from django.conf import settings
from django.core.management.commands.migrate import Command as DjangoMigrateCommand
from django.db import connection

from jsonfield_compat import is_db_postgresql


class Command(DjangoMigrateCommand):
    def handle(self, *args, **options):
        is_postgres = is_db_postgresql()
        create_table = getattr(settings, 'TEST_CREATE_DATA_AS_TEXT', False)
        if is_postgres and create_table:
            self.stdout.write('Creating MyModel table manually.')
            with connection.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE test_app_mymodel (
                         id serial NOT NULL,
                         data text,
                         CONSTRAINT test_app_mymodel_pkey PRIMARY KEY (id)
                       );"""
                )

        return super(Command, self).handle(*args, **options)


