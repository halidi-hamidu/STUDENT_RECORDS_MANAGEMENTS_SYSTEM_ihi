# Generated by Django 3.2.7 on 2021-09-24 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_student_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='status',
        ),
    ]
