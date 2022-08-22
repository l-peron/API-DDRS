from django.apps import apps, AppConfig
from django.contrib import admin


class CustomApp(AppConfig):
    name = 'ddrs_api'

    def ready(self):
        models = apps.get_models()
        for model in models:
            try:
                admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass
