from datetime import date

from django.contrib.auth.models import User, AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_born_date


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('occupation', 'ADMIN')

        if extra_fields.get('occupation') is not 'ADMIN':
            raise ValueError('Superuser must have occupation=ADMIN.')
        return super().create_superuser(username, email, password, **extra_fields)


class Profile(AbstractUser):
    OCCUPATION_TYPE = (
        ('FAC', _('Functionary of Migratory acts')),
        ('FUF', _('Functionary of Finance')),
        ('BDAC', _('Boss of Migratory acts')),
        ('DIR', _('Director')),
        ('ADMIN', _('Administrator')),
    )
    born_date = models.DateField(_('Born date'), blank=True, null=True, validators=[validate_born_date])
    occupation = models.CharField(_('Occupation'), max_length=5, choices=OCCUPATION_TYPE, default='FAC')

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def age(self):
        if self.born_date:
            return _('%(years)d years') % {'years': date.today().year - self.born_date.year}
        else:
            return None

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.username
