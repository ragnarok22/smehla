from django.db import models

CIVIL_STATUS = (
    ('c', 'Casado'),
    ('v', 'Viudo'),
    ('s', 'Soltero'),
)


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
