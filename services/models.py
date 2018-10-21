from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    CIVIL_STATUS = (
        ('S', _('Single')),
        ('E', _('Engaged')),
        ('M', _('Married')),
        ('W', _('Widower')),
    )

    def upload_file(self, filename):
        ext = filename.split('.')[-1]
        return 'clients/{}.{}'.format(self.ci, ext)

    ci = models.CharField(_('Identity card'), max_length=13, unique=True)
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=150)
    born_date = models.DateField(_('Born date'))
    civil_status = models.CharField(_('Civil status'), choices=CIVIL_STATUS, max_length=1)
    naturalness = models.CharField(_("Naturalness"), max_length=30)
    nationality = models.CharField(_('Nationality'), max_length=30)
    father = models.CharField(_('Father name'), max_length=200)
    mother = models.CharField(_('Mother name'), max_length=200)
    address = models.TextField(_('Address'))
    email = models.EmailField(_('Email'))
    phone = models.PositiveIntegerField(_('Phone number'))
    data_attachment = models.FileField(_('Data attachment'), upload_to=upload_file, null=True, blank=True)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()


class Service(models.Model):
    SERVICE_STATUS = (
        ('1', _('Request')),
        ('2', _('Invoicing')),
        ('3', _('Revision')),
        ('4', _('Authenticating')),
        ('5', _('Deliver')),
    )
    SERVICE_TYPE = {
        'None': _('Unknown service type'),
        'visa': _('Visa'),
    }
    client = models.ForeignKey(verbose_name=_('Client'), to=Client, on_delete=models.CASCADE)
    status = models.CharField(_('Status'), max_length=1, choices=SERVICE_STATUS)
    service_type = None

    def get_service_type(self):
        if self.service_type:
            return self.service_type
        else:
            return self.SERVICE_TYPE['None']

    def __str__(self):
        return self.service_type


class Visa(Service):
    REQUEST_SPECIFICATION = (
        ('VT', 'VT'),
        ('VPT', 'VPT'),
        ('VP', 'VP'),
        ('VE', 'VE'),
        ('VTM', 'VTM'),
        ('VOR', 'VOR'),
        ('VTU', 'VTU'),
        ('VCD', _('Visa of short duration')),
    )
    REQUEST_TYPE = (
        ('C', _('Caducity')),
        ('M', _('Misplacing')),
    )

    service_type = Service.SERVICE_TYPE['visa']
    specification = models.CharField(_('Specification'), max_length=3, choices=REQUEST_SPECIFICATION)
    extension_request_date = models.DateField(_('Extension request date'))
    request_type = models.CharField(_('Request type'), max_length=1, choices=REQUEST_TYPE)
    passport_no = models.CharField(_('Passport No.'), max_length=100)
    passport_issuance_date = models.DateField(_('Passport issuance date'))
    passport_expiration_date = models.DateField(_('Passport expiration date'))
    visa_no = models.CharField(_('Visa No.'), max_length=100)
    visa_issuance_date = models.DateField(_('Visa issuance date'))
    visa_expiration_date = models.DateField(_('Visa expiration date'))

    def __str__(self):
        return '{}: {} -> {}'.format(self.get_service_type(), self.client, self.specification)
