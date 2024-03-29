# Generated by Django 3.2.7 on 2021-09-23 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_course_course_credit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='module',
        ),
        migrations.AddField(
            model_name='course',
            name='module',
            field=models.ManyToManyField(blank=True, null=True, to='account.Module'),
        ),
        migrations.RemoveField(
            model_name='department',
            name='course',
        ),
        migrations.AddField(
            model_name='department',
            name='course',
            field=models.ManyToManyField(blank=True, null=True, to='account.Course'),
        ),
    ]
