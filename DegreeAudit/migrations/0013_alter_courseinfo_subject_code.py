# Generated by Django 4.2.6 on 2023-12-13 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DegreeAudit', '0012_alter_courseinfo_course_alter_courseinfo_pass_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinfo',
            name='subject_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DegreeAudit.subjectcode'),
        ),
    ]