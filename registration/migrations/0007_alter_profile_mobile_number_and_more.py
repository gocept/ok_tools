# Generated by Django 4.0.5 on 2022-07-12 11:08

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_alter_profile_okuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
