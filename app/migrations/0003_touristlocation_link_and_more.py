# Generated by Django 5.0 on 2024-12-14 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='touristlocation',
            name='link',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='seasonalpricing',
            unique_together={('category', 'start_date', 'end_date')},
        ),
    ]