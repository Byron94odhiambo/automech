# Generated by Django 5.1 on 2024-08-17 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='current_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='warranty_info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
