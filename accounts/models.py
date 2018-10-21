from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(AbstractUser):
    born_date = models.DateField(_('Born date'), blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'born_date']

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.username
