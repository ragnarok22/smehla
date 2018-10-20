from django.db import models

CIVIL_STATUS = (
    ('s', 'Soltero'),
    ('o', 'Comprometido'),
    ('c', 'Casado'),
    ('v', 'Viudo'),
)

REQUEST_SPECIFICATION = (
    ('VT', ''),
    ('VPT', ''),
    ('VP', ''),
    ('VE', ''),
    ('VTM', ''),
    ('VOR', ''),
    ('VTU', ''),
    ('VCD', ''),
)

REQUEST_TYPE = (
    ('C', 'Caducidad'),
    ('E', 'Extravio'),
)

SERVICE_STATUS = (
    ('1', 'Solicitud'),
    ('2', 'Facturacion'),
    ('3', 'Revision'),
    ('4', 'Autenticar'),
    ('5', 'Entrega'),
)

SERVICE_TYPE = {
    'visa': 'Visa',
}


class Client(models.Model):
    def upload_file(self, filename):
        ext = filename.split('.')[-1]
        return 'clients/{}.{}'.format(self.ci, ext)

    ci = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    born_date = models.DateField()
    civil_status = models.CharField(choices=CIVIL_STATUS, max_length=1)
    naturalness = models.CharField('Naturalidad', max_length=30)
    nationality = models.CharField('Nacionalidad', max_length=30)
    father = models.CharField(max_length=200)
    mother = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.PositiveIntegerField('Numero de telefono')
    data_attachment = models.FileField('Ficheros adjuntos', upload_to=upload_file)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service_type = None

    def get_service_type(self):
        if self.service_type:
            return self.service_type
        else:
            return 'Unknown service type'


class Visa(Service):
    service_type = SERVICE_TYPE['visa']
    specification = models.CharField('especificacion', max_length=3, choices=REQUEST_SPECIFICATION)
    extension_request_date = models.DateField('Pedido de prorroga')
    request_type = models.CharField('Tipo de solicitud', max_length=1, choices=REQUEST_TYPE)
    passport_no = models.CharField('No. de Pasaporte', max_length=100)
    passport_issuance_date = models.DateField('Fecha de emision de pasaporte')
    passport_expiration_date = models.DateField('Fecha de vencimiento de pasaporte')
    visa_no = models.CharField('No. de Visa', max_length=100)
    visa_issuance_date = models.DateField('Fecha de emision de Visa')
    visa_expiration_date = models.DateField('Fecha de vencimiento de Visa')
    status = models.CharField('Estado', max_length=1, choices=SERVICE_STATUS)
