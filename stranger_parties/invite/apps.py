from django.apps import AppConfig


class InviteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stranger_parties.invite"

    def ready(self):
        from . import signals  # noqa
