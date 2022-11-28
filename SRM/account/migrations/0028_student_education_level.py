# Generated by Django 3.2.7 on 2021-09-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_student_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='education_level',
            field=models.CharField(blank=True, choices=[('', 'select education level'), ('PHD', 'PHD'), ('MASTERS', 'MASTERS')], max_length=50, null=True),
        ),
    ]