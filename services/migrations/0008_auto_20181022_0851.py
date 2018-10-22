# Generated by Django 2.1.1 on 2018-10-22 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20181021_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visa',
            name='specification',
            field=models.CharField(choices=[('VT', 'Work visa'), ('VPT', 'Temporary stay visa'), ('VP', 'Privileged visa'), ('VE', 'Study visa'), ('VTM', 'Medical Treatment visa'), ('VOR', 'Ordinary visa'), ('VTU', 'Tourist visa'), ('VCD', 'Short-term visa')], max_length=3, verbose_name='Specification'),
        ),
    ]
