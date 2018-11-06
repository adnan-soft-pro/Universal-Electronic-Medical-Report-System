# Generated by Django 2.1 on 2018-10-30 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instructions', '0008_merge_20181025_1327'),
        ('accounts', '0002_auto_20181022_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientReportAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField(default=0)),
                ('token', models.CharField(max_length=6)),
                ('url', models.CharField(max_length=256)),
                ('instruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructions.Instruction')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Patient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
