# Generated by Django 5.0 on 2024-12-15 05:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]