# Generated by Django 2.1 on 2019-04-04 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20190401_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='key',
            field=models.CharField(max_length=255, verbose_name='Text'),
        ),
    ]
