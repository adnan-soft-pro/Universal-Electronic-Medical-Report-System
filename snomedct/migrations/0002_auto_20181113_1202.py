# Generated by Django 2.1 on 2018-11-13 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snomedct', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='readcode',
            name='snomedct_re_concept_458c16_idx',
        ),
        migrations.RemoveField(
            model_name='readcode',
            name='concept_id',
        ),
        migrations.AddField(
            model_name='snomedconcept',
            name='readcode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='snomed_concepts', to='snomedct.ReadCode'),
        ),
        migrations.AlterField(
            model_name='snomedconcept',
            name='children',
            field=models.ManyToManyField(related_name='snomed_concepts', through='snomedct.SnomedDescendant', to='snomedct.SnomedConcept'),
        ),
    ]
