# Generated by Django 3.2.7 on 2021-09-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_alter_student_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, choices=[('continuous', 'continuous'), ('postpone', 'postpone'), ('complete', 'complete')], default='continuous', max_length=50, null=True),
        ),
    ]