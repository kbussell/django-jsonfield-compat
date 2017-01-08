django-jsonfield-compat
=======================

Django 1.9 introduced first-class support for Postgresql's json type. 

Not everyone uses Postgresql, nor has upgraded to 1.9 yet, so a mixed ecosystem exists. 
Unfortunately, these two field types cannot be used together in the same project.

django-jsonfield-compat was created to be able to allow 3rd-party libraries to work in both worlds.

Caution
-------

This library is still under development and does not have tests yet.

Including this library may make modifications to your database! Use with caution!

Installation
------------

`pip install django-jsonfield-compat`

Adjust all instances of importing JSONField to jsonfield_compat's definition (including all migration files!)

```
from jsonfield_compat import JSONField
```

Register your app from the AppConfig class's `ready()` function.

Example `apps.py`:

```
from __future__ import unicode_literals

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'myapp'
    verbose_name = "My App"

    def ready(self):
        import jsonfield_compat
        jsonfield_compat.register_app(self)
```


Now, when users of your application want to switch from using django-jsonfield's implementation 
to Django's native JSONField, they add the setting:

```
USE_NATIVE_JSONFIELD = True
```

And then run migrations to convert the app's DB tables to use the JSON column type.


License
-------

django-jsonfield-compat is licensed under the MIT license (see the `LICENSE` file for details).
