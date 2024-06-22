from django.apps import AppConfig

class BackendDjangoConfig(AppConfig):
    name = 'backend_django'

    def ready(self):
        import backend_django.lookups
        print("Regsitered module")
