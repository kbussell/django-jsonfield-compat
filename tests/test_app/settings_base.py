"""
Settings file for jsonfield_compat tests
"""

SECRET_KEY = 'test'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'test_app',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'auditlog_tests.db',
    }
}

ROOT_URLCONF = []

JSONFIELD_ENCODER_CLASS = 'tests.test_app.json_encoder.TestJSONEncoder'
