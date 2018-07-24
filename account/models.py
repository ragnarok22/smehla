from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Profile(AbstractUser):
    born_date = models.DateField('Fecha de nacimiento', blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.username
