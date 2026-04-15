from django.apps import AppConfig


class InteractionsConfig(AppConfig):
    name = 'interactions'

class InteractionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interactions'

    def ready(self):
        import backend.interactions.signals
