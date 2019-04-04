# Generated by Django 2.1 on 2019-04-04 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_auto_20190404_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyinvoice',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total cost invoice'),
        ),
    ]
