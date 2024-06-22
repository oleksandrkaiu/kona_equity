from django.contrib import admin
from .models import Company, Tasks, IP

# Register your models here.
admin.site.register(Company)
admin.site.register(Tasks)
admin.site.register(IP)
