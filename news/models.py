from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    content = models.TextField(_('Content'))
    pub_date = models.DateField(_('Publication date'), auto_now=True)

    def __str__(self):
        return self.title
