# Generated by Django 3.2.7 on 2021-09-24 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20210924_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(blank=True, max_length=100, null=True)),
                ('college_location', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'colleges',
            },
        ),
        migrations.AlterField(
            model_name='student',
            name='programme_name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.college'),
        ),
    ]