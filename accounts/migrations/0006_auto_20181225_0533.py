# Generated by Django 2.1 on 2018-12-25 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20181204_0829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalpracticeuser',
            name='can_complete_amra',
        ),
        migrations.RemoveField(
            model_name='generalpracticeuser',
            name='can_complete_sars',
        ),
    ]
