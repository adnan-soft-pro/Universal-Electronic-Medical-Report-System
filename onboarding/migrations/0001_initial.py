# Generated by Django 2.1 on 2018-11-13 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EMRSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('surgery_name', models.CharField(max_length=255)),
                ('surgery_code', models.CharField(max_length=255)),
                ('surgery_email', models.EmailField(max_length=255)),
                ('address_line1', models.CharField(max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('post_code', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('pm_name', models.CharField(max_length=255)),
                ('pm_email', models.EmailField(max_length=255)),
                ('receive_email', models.EmailField(blank=True, max_length=255)),
                ('gp_name', models.CharField(max_length=255)),
                ('primary_care', models.CharField(choices=[('EMISWeb', 'EMIS-Web'), ('HealthyV5', 'Healthy V5'), ('LV', 'EMIS-LV'), ('PCS', 'PCS'), ('Practice Manager', 'Practice Manager'), ('PREMIERE', 'Premiere'), ('SYNERGY', 'Synergy'), ('SystmOne', 'SystmOne'), ('Vision 3', 'Vision 3'), ('VA', 'Vision Anywhere'), ('MT', 'Microtest'), ('OT', 'Other')], max_length=2)),
                ('person_completeing', models.CharField(max_length=255)),
                ('job_title', models.CharField(blank=True, max_length=255)),
                ('accept_policy', models.BooleanField(default=False)),
                ('consented', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
