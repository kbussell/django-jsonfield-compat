from django.apps import AppConfig


class JSONFieldCompatTestConfig(AppConfig):
    name = 'test_app'

    def ready(self):
        import jsonfield_compat

        jsonfield_compat.register_app(self)
