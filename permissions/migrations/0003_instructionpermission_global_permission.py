# Generated by Django 2.1 on 2018-12-04 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_auto_20181204_0406'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionpermission',
            name='global_permission',
            field=models.BooleanField(default=False),
        ),
    ]
