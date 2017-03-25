import os
from test_app.settings_base import *  # NOQA

USE_NATIVE_JSONFIELD = True

TEST_CREATE_DATA_AS_TEXT = True

_db = os.environ.get('DB', 'postgresql')
if _db == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'jsonfield_compat',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

