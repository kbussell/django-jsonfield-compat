Changelog
=========

0.4.4 - 03/25/2017
------------------

 - Fix path in deconstruct() call

0.4.3 - 03/25/2017
------------------

 - Add deconstruct() call to model to prevent spurious migrations

0.4.2 - 03/25/2017
------------------

 - Add Django 1.8 support

0.4.1 - 03/25/2017
------------------

 - Fix pypi upload (no code changes)

0.4.0 - 03/25/2017
------------------

  - **Backwards incompatible change** JSONFormField has been moved to `jsonfield_compat.forms.JSONFormField`
  - More tests
  - Travis, coveralls integration

0.3.0 - 01/09/2017
------------------

  - Support `JSONFormField`s

0.2.0 - 01/08/2017
------------------

  - Subclass Django's native `JSONField` to override the json encoder with the `JSONFIELD_ENCODER_CLASS` setting

0.1.0 - 01/08/2017
------------------

  - Initial release
