from jsonfield_compat.util import use_native_jsonfield

if use_native_jsonfield():
    from django.contrib.postgres.fields import JSONField as _JSONFormField
else:
    from jsonfield.forms import JSONFormField as _JSONFormField

JSONFormField = _JSONFormField
