from django.contrib import admin
from services import models

admin.site.register(models.Client)
admin.site.register(models.Service)
admin.site.register(models.Visa)
admin.site.register(models.Passport)
admin.site.register(models.Entity)
admin.site.register(models.ResidenceAuthorization)
admin.site.register(models.ResidenceMarriage)
admin.site.register(models.ResidenceRenovation)
