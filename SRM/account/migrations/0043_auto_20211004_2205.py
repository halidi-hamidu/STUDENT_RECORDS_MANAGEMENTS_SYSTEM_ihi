# Generated by Django 3.1.5 on 2021-10-04 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0042_auto_20210930_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='module',
        ),
        migrations.DeleteModel(
            name='Module',
        ),
    ]
