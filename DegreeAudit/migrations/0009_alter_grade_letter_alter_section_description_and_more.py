# Generated by Django 4.2.6 on 2023-12-13 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DegreeAudit', '0008_alter_section_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='letter',
            field=models.CharField(max_length=4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='section',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.CharField(max_length=9)),
                ('student_name', models.CharField(max_length=200)),
                ('student_surname', models.CharField(max_length=200)),
                ('student_study_year', models.IntegerField()),
                ('adviser', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='DegreeAudit.ugmajor')),
            ],
            options={
                'db_table': 'da_student_info',
            },
        ),
    ]