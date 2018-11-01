# Generated by Django 2.1.1 on 2018-11-01 01:51

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_occupation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='born_date',
            field=models.DateField(blank=True, null=True, validators=[accounts.validators.validate_born_date], verbose_name='Born date'),
        ),
    ]
