# Generated by Django 2.1 on 2018-10-17 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snomedct', '0003_auto_20181016_1319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snomedconcept',
            old_name='child',
            new_name='children',
        ),
    ]