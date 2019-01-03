# Generated by Django 2.1 on 2018-12-28 04:14

from django.db import migrations, models
import django_clamd.validators


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0016_auto_20181226_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruction',
            name='consent_form',
            field=models.FileField(blank=True, null=True, upload_to='consent_forms', validators=[django_clamd.validators.validate_file_infection]),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='mdx_consent',
            field=models.FileField(blank=True, null=True, upload_to='consent_forms', validators=[django_clamd.validators.validate_file_infection]),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='medical_report',
            field=models.FileField(blank=True, null=True, upload_to='medical_reports', validators=[django_clamd.validators.validate_file_infection]),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='sars_consent',
            field=models.FileField(blank=True, null=True, upload_to='consent_forms', validators=[django_clamd.validators.validate_file_infection]),
        ),
        migrations.AlterField(
            model_name='setting',
            name='consent_form',
            field=models.FileField(blank=True, null=True, upload_to='consent_forms', validators=[django_clamd.validators.validate_file_infection]),
        ),
    ]