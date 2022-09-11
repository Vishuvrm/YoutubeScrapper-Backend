from django.apps import AppConfig

class ScrapConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scrap"

    def ready(self):
        from  .scheduled_updater import start, delete_channel_data
        start(job=delete_channel_data, interval=60)
