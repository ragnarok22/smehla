from datetime import date

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Profile(AbstractUser):
    OCCUPATION_TYPE = (
        ('FAC', _('Functionary of Attention to Customer')),
        ('BAC', _('Boss of Attention to Customer')),
        ('BDAC', _('Boss of Departament of Attention to Customer')),
        ('DIR', _('Director')),
        ('ADMIN', _('Administrator')),
    )
    born_date = models.DateField(_('Born date'), blank=True, null=True)
    occupation = models.CharField(_('Occupation'), max_length=5, choices=OCCUPATION_TYPE, default=OCCUPATION_TYPE[0])

    REQUIRED_FIELDS = ['email', 'born_date']

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
