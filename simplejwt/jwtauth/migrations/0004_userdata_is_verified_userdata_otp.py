# Generated by Django 5.1 on 2024-08-12 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtauth', '0003_remove_userdata_is_verified_remove_userdata_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdata',
            name='otp',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
