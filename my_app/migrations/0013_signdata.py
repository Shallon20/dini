# Generated by Django 5.1.3 on 2025-03-19 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0012_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('x_values', models.TextField()),
                ('y_values', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
