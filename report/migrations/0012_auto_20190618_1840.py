# Generated by Django 2.1 on 2019-06-18 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0011_auto_20190519_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientreportauth',
            name='report_de_activate',
            field=models.BooleanField(default=True),
        ),
    ]
