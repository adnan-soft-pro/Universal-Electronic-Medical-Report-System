# Generated by Django 2.1 on 2019-05-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0010_unsupportedattachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unsupportedattachment',
            name='created',
        ),
        migrations.RemoveField(
            model_name='unsupportedattachment',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='unsupportedattachment',
            name='modified',
        ),
        migrations.AddField(
            model_name='patientreportauth',
            name='report_de_activate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unsupportedattachment',
            name='file_content',
            field=models.BinaryField(default=b''),
            preserve_default=False,
        ),
    ]
