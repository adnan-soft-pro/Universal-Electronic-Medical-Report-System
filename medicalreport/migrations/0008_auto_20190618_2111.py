# Generated by Django 2.1 on 2019-06-18 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalreport', '0007_auto_20190519_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amendmentsforrecord',
            old_name='raw_medical_xml',
            new_name='_raw_medical_xml_encrypted',
        ),
        migrations.AddField(
            model_name='amendmentsforrecord',
            name='_raw_medical_xml_aes_key',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='amendmentsforrecord',
            name='raw_medical_xml_aes_key_salt_and_encrypted_iv',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='amendmentsforrecord',
            name='raw_medical_xml_salt_and_encrypted_iv',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
