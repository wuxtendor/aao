# Generated by Django 4.2.6 on 2023-12-12 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DegreeAudit', '0005_alter_subjectchoice_levels'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='subject_codes',
            field=models.ManyToManyField(to='DegreeAudit.subjectcode'),
        ),
    ]
