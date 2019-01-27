from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    def picture_news(self, filename):
        ext = filename.split('.')[-1]
        return 'news/{}/{}.{}'.format(self.pub_date, self.title, ext)

    picture = models.ImageField(_('Picture'), upload_to=picture_news)
    title = models.CharField(_('Title'), max_length=100)
    content = models.TextField(_('Content'))
    pub_date = models.DateField(_('Publication date'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')


class Service(models.Model):
    def file_services(self, filename):
        ext = filename.split('.')[-1]
        return 'services/{}.{}'.format(self.service_type, ext)

    service_type = models.CharField(_('Service Type'), max_length=100)
    description = models.CharField(_('Description'), max_length=250)
    file = models.FileField(_('File'), upload_to=file_services)

    def __str__(self):
        return self.service_type

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Legislation(models.Model):
    def file_legislation(self, filename):
        ext = filename.split('.')[-1]
        return 'legislation/{}.{}'.format(self.service_type, ext)

    service_type = models.CharField(_('Legislation Type'), max_length=100)
    description = models.CharField(_('Description'), max_length=250)
    file = models.FileField(_('File'), upload_to=file_legislation)

    def __str__(self):
        return self.service_type

    class Meta:
        verbose_name = _('Legislation')
        verbose_name_plural = _('Legislation')
