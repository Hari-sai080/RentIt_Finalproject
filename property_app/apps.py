from django.apps import AppConfig

class PropertyAppConfig(AppConfig):
    name = 'property_app'

    def ready(self):
        import property_app.signals  # This registers your signals without running any DB queries immediately.
