# Generated by Django 2.1 on 2019-06-24 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_auto_20190528_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryhistory',
            name='xpath',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]