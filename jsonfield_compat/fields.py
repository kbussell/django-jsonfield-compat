from jsonfield_compat.util import use_native_jsonfield

if use_native_jsonfield():
    from jsonfield_compat.compat import _JSONField
else:
    from jsonfield.fields import JSONField as _JSONField

JSONField = _JSONField
