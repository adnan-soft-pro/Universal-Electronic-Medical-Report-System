# Generated by Django 2.1 on 2019-05-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0050_auto_20190430_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruction',
            name='status',
            field=models.IntegerField(choices=[(0, 'New'), (1, 'In Progress'), (2, 'Completed'), (3, 'Rejected'), (4, 'Paid'), (5, 'Finalising'), (6, 'Fail'), (7, 'Redacting')], default=0),
        ),
    ]
