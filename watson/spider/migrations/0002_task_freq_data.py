# Generated by Django 3.1.4 on 2020-12-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='freq_data',
            field=models.JSONField(default=dict),
        ),
    ]
