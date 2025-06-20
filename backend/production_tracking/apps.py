from django.apps import AppConfig


class ProductionTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'production_tracking'

    def ready(self):
        import production_tracking.signals
