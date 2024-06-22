from django.apps import AppConfig

class BackendDjangoConfig(AppConfig):
    name = 'backend_django'

    def ready(self):
        import backend_django.lookups
        print("Regsitered module")



        " /home/Konaequity/.virtualenvs/updatedvenv/bin/python /home/Konaequity/manage.py update_hubspot --sleep 15 " 