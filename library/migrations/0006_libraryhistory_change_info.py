# Generated by Django 2.1 on 2019-04-26 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20190425_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryhistory',
            name='change_info',
            field=models.TextField(blank=True, verbose_name='Change information'),
        ),
    ]