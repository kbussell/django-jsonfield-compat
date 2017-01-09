from settings_base import *  # NOQA

USE_NATIVE_JSONFIELD = True

TEST_CREATE_DATA_AS_TEXT = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jsonfield_compat',
        'USER': 'e3',
        'PASSWORD': 'e3',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
