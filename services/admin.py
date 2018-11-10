from django.contrib import admin
from services import models

admin.site.register(models.Client)
admin.site.register(models.Service)
admin.site.register(models.Visa)
admin.site.register(models.Passport)
