from django.contrib import admin
from services import models

admin.site.register(models.Client)
admin.site.register(models.Service)
admin.site.register(models.Passport)
admin.site.register(models.ResidenceAuthorization)
admin.site.register(models.Visa)
admin.site.register(models.ExtensionVisa)
admin.site.register(models.MedicalTreatmentVisa)
admin.site.register(models.StudyVisa)
admin.site.register(models.TemporaryVisa)
