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

    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=150)
    born_date = models.DateField(_('Born date'), validators=[validators.validate_born_date])
    civil_status = models.CharField(_('Civil status'), choices=CIVIL_STATUS, max_length=1)
    sex = models.CharField(_('Sex'), max_length=1, choices=SEX_CHOICES)
    picture = models.ImageField(_('Picture'), upload_to=upload_image, null=True, blank=True)
    father = models.CharField(_('Father name'), max_length=200)
    mother = models.CharField(_('Mother name'), max_length=200)
    email = models.EmailField(_('Email'))
    phone = models.PositiveIntegerField(_('Phone number'))
    data_attachment = models.FileField(_('Data attachment'), upload_to=upload_file, null=True, blank=True)
    # Work data
    profession = models.CharField(_('Profession'), max_length=200)
    funcion = models.CharField(_('Function'), max_length=200, null=True, blank=True)
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
        'extension': _('Visa Extension'),
        'passport': _('Passport'),
        'residence': _('Residence authorization'),
    }
    client = models.ForeignKey(verbose_name=_('Client'), to=Client, on_delete=models.CASCADE)
    status = models.CharField(_('Status'), max_length=1, choices=SERVICE_STATUS, default='1')
    service_type = None
    process_no = models.PositiveSmallIntegerField()
    official = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Official'))

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
    REQUEST_TYPE_CHOICES = (
        ('WV', _('Work visa')),
        ('PV', _('Privileged visa')),
        ('RV', _('Resident visa')),
        ('SV', _('Study visa')),
        ('MTV', _('Medical Treatment visa')),
        ('TSV', _('Temporary stay visa')),
        ('STV', _('Short-term visa')),
        ('TV', _('Tourist visa')),
        ('OV', _('Ordinary visa')),
    )

    service_type = 'visa'
    request_type = models.CharField(_('Request type'), max_length=3, choices=REQUEST_TYPE_CHOICES)
    # Client data
    place_of_birth = models.CharField(_('Place of birth'), max_length=100)
    birth_country = models.CharField(_('Birth country'), max_length=100)
    nationality = models.CharField(_('Origin nationality'), max_length=100)
    current_nationality = models.CharField(_('Current nationality'), max_length=100)
    # passport data
    passport_no = models.CharField(_('Passport No.'), max_length=100)
    passport_issuance_place = models.CharField(_('Passport issuance place'), max_length=100)
    passport_issuance_date = models.DateField(_('Passport issuance date'))
    passport_expiration_date = models.DateField(_('Passport expiration date'))

    father_nationality = models.CharField(_('Father nationality'), max_length=100)
    mother_nationality = models.CharField(_('Mother nationality'), max_length=100)
    lodging = models.CharField(_('Lodging'), max_length=100)  # hospedaje
    city_lodging = models.CharField(_('City lodging'), max_length=100)
    street_lodging = models.CharField(_('Street lodging'), max_length=100)
    no_lodging_house = models.CharField(_('Lodging house No.'), max_length=5)
    last_entry_angola_date = models.DateField(_('Last entry angola date'))
    frontier = models.CharField(_('Frontier used'), max_length=100)
    visa_expiration_date = models.DateField(_('Visa expiration date'))

    class Meta:
        verbose_name = _('Visa')
        verbose_name_plural = _('Visas')

    def __str__(self):
        return '{}: {} -> {}'.format(self.get_service_type(), self.client, self.get_request_type_display())


class WorkVisa(Visa):
    # if is a work visa
    organism_name = models.CharField(_('Organism name'), max_length=100)
    organism_address = models.CharField(_('Organism address'), max_length=100)
    funcion = models.CharField(_('Funtion'), max_length=100)
    init_contract_date = models.DateField(_('Init contract date'))
    end_contract_date = models.DateField(_('End contract date'))
    entity_name = models.CharField(_('Entity name'), max_length=100)
    entity_address = models.CharField(_('Entity address'), max_length=100)


class MedicalTreatmentVisa(Visa):
    # if is a medical treatment visa
    UNITY_TYPE_CHOICES = (
        ('P', _('Public')),
        ('V', _('Private')),
    )
    unity_medical_name = models.CharField(_('Unity medical name'), max_length=100)
    unity_type = models.CharField(_('Unity type'), max_length=1, choices=UNITY_TYPE_CHOICES)
    date_init_treatment = models.DateField(_('Date init treatment'))
    data_end_treatment = models.DateField(_('Date end treatment'))


class ResidentVisa(Visa):
    # if is a fijacion de residencia
    reason = models.TextField(_('Reason'))
    TYPE_RESIDENCE_CHOICES = (
        ('T', _('Temporary')),
        ('P', _('Permanent')),
    )
    type_residence = models.CharField(_('Type residence'), max_length=1, choices=TYPE_RESIDENCE_CHOICES)
    LIVE_FAMILIAR_CHOICES = (
        ('Y', _('Yes')),
        ('N', _('No')),
        ('W', _('Wife')),
        ('H', _('Husband')),
        ('C', _('Children')),
        ('O', _('Others')),
    )
    live_familiar = models.CharField(_('Live with a familiar'), max_length=1, choices=LIVE_FAMILIAR_CHOICES)
    familiars = models.TextField(_('Familiars'))
    subsistence = models.TextField(_('Subsistence'))
    address_angola = models.CharField(_('Address angola'), max_length=100)


class TemporaryVisa(Visa):
    # if is a temporary visa
    REASON_CHOICES = (
        ('HR', _('Humanitarian reason')),
        ('RI', _('Mission in favor of a religious institution')),
        ('SR', _('Carrying out scientific research')),
        ('FA', _('Family Accompaniment')),
        ('VR', _('Familiar with a valid residence permit holder')),
        ('MC', _('Spouse of national citizen')),
    )
    reason = models.CharField(_('Reason'), max_length=2, choices=REASON_CHOICES)
    subsistence = models.TextField(_('Subsistence'))
    address_angola = models.TextField(_('address angola'))


class PrivilegedVisa(Visa):
    # if is a privileged visa
    research_company = models.CharField(_('Research company'), max_length=100)
    CONDITION_CHOICES = (
        ('R', _('Research')),
        ('E', _('Represent')),
        ('P', _('Procurator')),
    )
    condition = models.CharField(_('Condition'), max_length=1, choices=CONDITION_CHOICES)
    address_angola = models.CharField(_('address angola'), max_length=100)


class StudyVisa(Visa):
    # if is a study visa
    STUDY_PROGRAM_CHOICES = (
        ('P', _('Private')),
        ('U', _('Public')),
        ('F', _('Professional training to obtain an academic or professional degree')),
    )
    STAGES_CHOICES = (
        ('PC', _('Private companies')),
        ('UC', _('Public companies')),
    )
    study_program = models.CharField(_('Study program'), max_length=1, choices=STUDY_PROGRAM_CHOICES)
    init_date = models.DateField(_('Init date'))
    end_date = models.DateField(_('End date'))
    stages_in = models.CharField(_('internships in'), max_length=2, choices=STAGES_CHOICES)


class ExtensionVisa(Visa):
    visa_no = models.CharField(_('Visa No.'), max_length=20)
    valid_date = models.DateField(_('Valid date'))
    reason_extension = models.CharField(_('Reason extension'), max_length=250)
    cant_days_extension = models.PositiveIntegerField(_('Number of days of extension'))


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
    extension_type = models.CharField(_('Extension type'), max_length=2, choices=EXTENSION_TYPE_CHOICES, null=True,
                                      blank=True)
    observations = models.TextField(_('Observations'))
    # clients data
    naturalness = models.CharField(_('Naturalness'), max_length=100)
    nationality = models.CharField(_('Nationality'), max_length=100)
    passport_no = models.CharField(_('Passport No.'), max_length=14)
    passport_issued_in = models.CharField(_('Passport issued in'), max_length=100)
    date_issuance_passport = models.DateField(_('Date of issuance of passport'))
    father_nationality = models.CharField(_('Father nationality'), max_length=100)
    mother_nationality = models.CharField(_('Mother nationality'), max_length=100)
    # for non-local use of the reception
    location = models.CharField(_('Location'), max_length=100)
    date = models.DateField(_("Date"))
    # for official use
    date_official_use = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Residence authorization')
        verbose_name_plural = _('Authorization of residences')


class Passport(Service):
    PASSPORT_TYPE = (
        ('E', _('Emission')),
        ('R', _('Remission')),
    )
    REMISSION_TYPE_CHOICES = (
        ('BC', _('Bad conservation')),
        ('LT', _('Lost/Theft')),
        ('PE', _('Page exhaustion')),
        ('EX', _('Expiration')),
    )
    service_type = 'passport'
    passport_type = models.CharField(_('Passport type'), max_length=1, choices=PASSPORT_TYPE)
    remission_type = models.CharField(_('Remission type'), max_length=2, choices=REMISSION_TYPE_CHOICES, blank=True,
                                      null=True)
    # birth certificate
    issued_in = models.CharField(_('Issued in'), max_length=100)
    # identity card
    date = models.DateField(_('Date'))  # ver a candido esta fecha de que es
    cp = models.CharField(_('Cédula pessoal'), max_length=4)
    cp_issued_in = models.CharField(_('Indentity card issued in'), max_length=100)
    date_cp_issue = models.DateField(_('Date of cédula pessoal issue'))
    ci = models.CharField(_('Identity card'), max_length=14)
    ci_issued_in = models.CharField(_('Identity card issued in'), max_length=100)
    spouse = models.CharField(_('Spouse'), max_length=200, null=True, blank=True)
    observations = models.TextField(_('Observations'), null=True, blank=True)
    # client data
    # birth address
    province_birth = models.CharField(_('Province'), max_length=50)
    municipality_birth = models.CharField(_('Municipality'), max_length=50)
    commune_birth = models.CharField(_('Commune'), max_length=50)
    neighborhood_birth = models.CharField(_('Neighborhood'), max_length=50)
    street_birth = models.CharField(_('Street'), max_length=50)
    home_no_birth = models.CharField(_('Home No.'), max_length=10)
    # for use of the reception
    date_reception = models.DateField(_('Date'))
    # for official use
    passport_no = models.CharField(_('Pasport No.'), max_length=100)
    passport_issued_in = models.CharField(_('Passport issued in'), max_length=100)
    date_issue_passport = models.DateField(_('Date issue passport'))

    class Meta:
        verbose_name = _('passport')
        verbose_name_plural = _('passports')

    def __str__(self):
        return '{}-> passport type: {}'.format(self.client, self.get_passport_type_display())
