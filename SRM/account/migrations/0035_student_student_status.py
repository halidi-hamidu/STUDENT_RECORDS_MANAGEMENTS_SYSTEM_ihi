# Generated by Django 3.1.5 on 2021-09-25 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_remove_student_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_status',
            field=models.CharField(blank=True, choices=[('continuous', 'continuous'), ('postpone', 'postpone'), ('complete', 'complete'), ('final', 'final')], max_length=50, null=True),
        ),
    ]
