# Generated by Django 3.2.7 on 2021-09-23 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20210923_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_credit',
        ),
    ]
