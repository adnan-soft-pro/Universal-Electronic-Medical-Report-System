# Generated by Django 2.1 on 2018-12-07 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0008_instruction_medical_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionpatient',
            name='patient_dob_day',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='instructionpatient',
            name='patient_dob_month',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='instructionpatient',
            name='patient_dob_year',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]