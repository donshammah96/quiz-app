# Generated by Django 3.2.25 on 2025-01-05 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0002_auto_20250105_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='results',
            field=models.JSONField(default=dict),
        ),
    ]