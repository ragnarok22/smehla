from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile
from services import validators


class Client(models.Model):
    CIVIL_STATUS = (
        ('S', _('Single')),
        ('M', _('Married')),
        ('W', _('Widower')),
        ('D', _('Divorced')),
    )
    SEX_CHOICES = (
        ('M', _('Man')),
        ('W', _('Woman')),
    )

    def upload_file(self, filename):
        ext = filename.split('.')[-1]
        return 'clients/{}.{}'.format(self.get_full_name(), ext)

    def upload_image(self, filename):
        ext = filename.split('.')[-1]
        return 'clients/picture/{}.{}'.format(self.get_full_name(), ext)

    first_name = models.CharField(_('First name'), max_length=30)  # ok
    last_name = models.CharField(_('Last name'), max_length=150)  # ok
    born_date = models.DateField(_('Born date'), validators=[validators.validate_born_date])  # ok
    civil_status = models.CharField(_('Civil status'), choices=CIVIL_STATUS, max_length=1)  # ok
    sex = models.CharField(_('Sex'), max_length=1, choices=SEX_CHOICES)
    picture = models.ImageField(_('Picture'), upload_to=upload_image, null=True, blank=True)  # ok
    father = models.CharField(_('Father name'), max_length=200)  # ok
    mother = models.CharField(_('Mother name'), max_length=200)  # ok
    email = models.EmailField(_('Email'))  # ok
    phone = models.PositiveIntegerField(_('Phone number'))  # ok
    data_attachment = models.FileField(_('Data attachment'), upload_to=upload_file, null=True, blank=True)  # ok
    # Work data
    profession = models.CharField(_('Profession'), max_length=200)
    funcion = models.CharField(_('Function'), max_length=200)
    work_name = models.CharField(_('Work name'), max_length=200)
    # Current Address
    province = models.CharField(_('Province'), max_length=50)
    municipality = models.CharField(_('Municipality'), max_length=50)
    commune = models.CharField(_('Commune'), max_length=50)
    neighborhood = models.CharField(_('Neighborhood'), max_length=50)
    street = models.CharField(_('Street'), max_length=50)
    home_no = models.CharField(_('Home No.'), max_length=10)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

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
        'passport': _('Passport'),
        'residence': _('Residence authorization'),
    }
    client = models.ForeignKey(verbose_name=_('Client'), to=Client, on_delete=models.CASCADE)  # ok
    status = models.CharField(_('Status'), max_length=1, choices=SERVICE_STATUS, default='1')
    service_type = None
    type_request = models.CharField(_('Type request'), max_length=3)
    process_no = models.PositiveSmallIntegerField()

    def get_service_type(self):
        if self.service_type:
            return self.SERVICE_TYPE[self.service_type]
        else:
            return self.SERVICE_TYPE['None']

    def can_mod(self, user):
        if user:
            if (self.status == '1' and user.occupation == 'FAC') or (
                    self.status == '2' and user.occupation == 'BAC') or (
                    self.status == '3' and user.occupation == 'BDAC') or (
                    self.status == '4' and user.occupation == 'DIR'):
                return True
        return False

    def get_previous_status(self):
        if self.status == '2':
            return self.SERVICE_STATUS[0][1]
        elif self.status == '3':
            return self.SERVICE_STATUS[1][1]
        elif self.status == '4':
            return self.SERVICE_STATUS[2][1]
        elif self.status == '5':
            return self.SERVICE_STATUS[3][1]
        else:
            return None

    def get_next_status(self):
        if self.status == '1':
            return self.SERVICE_STATUS[1][1]
        elif self.status == '2':
            return self.SERVICE_STATUS[2][1]
        elif self.status == '3':
            return self.SERVICE_STATUS[3][1]
        elif self.status == '4':
            return self.SERVICE_STATUS[4][1]
        else:
            return None

    def __str__(self):
        return '{}'.format(self.get_service_type())


class Visa(Service):
    REQUEST_SPECIFICATION = (
        ('VT', _('Work visa')),
        ('VPT', _('Temporary stay visa')),
        ('VP', _('Privileged visa')),
        ('VE', _('Study visa')),
        ('VTM', _('Medical Treatment visa')),
        ('VOR', _('Ordinary visa')),
        ('VTU', _('Tourist visa')),
        ('VCD', _('Short-term visa')),
    )
    REQUEST_TYPE = (
        ('N', _('Normal')),
        ('C', _('Caducity')),
        ('M', _('Misplacing')),
    )

    service_type = 'visa'
    specification = models.CharField(_('Specification'), max_length=3, choices=REQUEST_SPECIFICATION)
    extension_request_date = models.DateField(_('Extension request date'))
    request_type = models.CharField(_('Request type'), max_length=1, choices=REQUEST_TYPE)
    passport_no = models.CharField(_('Passport No.'), max_length=100)
    passport_issuance_date = models.DateField(_('Passport issuance date'))
    passport_expiration_date = models.DateField(_('Passport expiration date'))
    visa_no = models.CharField(_('Visa No.'), max_length=100)
    visa_issuance_date = models.DateField(_('Visa issuance date'))
    visa_expiration_date = models.DateField(_('Visa expiration date'))
    tutelary_entity = models.ForeignKey('Entity', verbose_name=_('Tutelary Entity'), on_delete=models.CASCADE,
                                        blank=True, null=True)

    class Meta:
        verbose_name = _('Visa')
        verbose_name_plural = _('Visas')

    def __str__(self):
        return '{}: {} -> {}'.format(self.get_service_type(), self.client, self.get_specification_display())


class ResidenceAuthorization(Service):  # in progress to fixed
    TYPE_REQUEST_CHOICES = (
        ('TTA', _('Temporary type A')),
        ('TTB', _('Temporary type B')),
        ('PER', _('Permanent')),
        ('EMI', _('Emission')),
        ('EXT', _('Extension')),
    )
    EXTENSION_TYPE_CHOICES = (
        ('BC', _('Bad conservation')),
        ('LT', _('Lost/Theft')),
        ('EX', _('Expiration')),
    )
    service_type = 'residence'
    type_request = models.CharField(_('Type request'), max_length=3, choices=TYPE_REQUEST_CHOICES)
    extension_type = models.CharField(_('Extension type'), choices=EXTENSION_TYPE_CHOICES)
    observations = models.TextField(_('Observations'))
    # clients data
    naturalness = models.CharField(_('Naturalness'), max_length=100)
    nationality = models.CharField(_('Nationality'), max_length=100)
    passport_no = models.CharField(_('Passsport No.'), max_length=14)
    passport_issued_in = models.CharField(_('Passport issued in'), max_length=100)
    date_issuance_passport = models.DateField(_('Date of issuance of passport'))
    father_nationality = models.CharField(_('Father nationality'), max_length=100)
    mother_nationality = models.CharField(_('Father nationality'), max_length=100)
    # for non-local use of the reception
    location = models.CharField(_('Location'), max_length=100)
    date = models.DateField(_("Date"))
    official = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Official'))
    # for official use
    date_official_use = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Residence authorization')
        verbose_name_plural = _('Authorization of residences')


class Passport(Service):
    PASSPORT_TYPE = (
        ('N', _('Normal')),
        ('S', _('Service')),
    )
    service_type = 'passport'
    passport_type = models.CharField(_('Passport type'), max_length=1, choices=PASSPORT_TYPE)
    emission_date = models.DateField(_('Emission date'))
    remission_type = models.CharField(_('Remission type'), max_length=1, choices=Visa.REQUEST_TYPE)
    remission_date = models.DateField(_('Remission date'))
    personal_no = models.CharField(_('Personal No.'), max_length=50)
    passport_no = models.CharField(_('Passport No.'), max_length=100)
    passport_issuance_date = models.DateField(_('Passport issuance date'))
    passport_expiration_date = models.DateField(_('Passport expiration date'))

    class Meta:
        verbose_name = _('passport')
        verbose_name_plural = _('passports')

    def __str__(self):
        return '{}-> passport type: {}'.format(self.client, self.get_passport_type_display())


class Entity(models.Model):
    class Meta:
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')

    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField(_('Name'), max_length=100)
    localization = models.CharField(_('Localization'), max_length=200)
    identification_no = models.CharField(_('Identification No.'), max_length=50)
    issuance_date = models.DateField(_('Issuance date'))
    expiration_date = models.DateField(_('Expiration date'))
    telephone = models.PositiveIntegerField(_('Telephone'))
    email = models.EmailField(_('Email'))

    def to_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'localization': self.localization,
            'identification_no': self.identification_no,
            'issuance_date': self.issuance_date,
            'expiration_date': self.expiration_date,
            'telephone': self.telephone,
            'email': self.email,
        }
