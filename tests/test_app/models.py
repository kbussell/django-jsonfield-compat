from django.db import models

from jsonfield_compat import JSONField


class MyModel(models.Model):
    data = JSONField()
