# Generated by Django 5.1.3 on 2025-02-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0006_interpreterapplication_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpreterapplication',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interpreterapplication',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interpreterapplication',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interpreterapplication',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]
