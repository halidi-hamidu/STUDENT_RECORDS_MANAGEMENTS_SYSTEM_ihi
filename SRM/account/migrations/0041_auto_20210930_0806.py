# Generated by Django 3.1.5 on 2021-09-30 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0040_auto_20210930_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_status',
            field=models.CharField(blank=True, choices=[('None', 'Status'), ('continuous', 'continuous'), ('postpone', 'postpone'), ('complete', 'complete'), ('final', 'final')], max_length=50, null=True),
        ),
    ]