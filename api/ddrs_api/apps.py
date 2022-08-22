from django.apps import apps, AppConfig
from django.contrib import admin


class DdrsApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ddrs_api'

    def ready(self):
        models = self.get_models()
        for model in models:
            try:
                admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass
