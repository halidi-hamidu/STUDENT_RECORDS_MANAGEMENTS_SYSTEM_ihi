# Generated by Django 3.2.7 on 2021-09-24 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_student_education_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_status',
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('', 'select gender'), ('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True),
        ),
    ]
