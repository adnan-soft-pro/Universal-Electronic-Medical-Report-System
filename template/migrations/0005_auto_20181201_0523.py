# Generated by Django 2.1 on 2018-12-01 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0004_auto_20181201_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateinstruction',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
