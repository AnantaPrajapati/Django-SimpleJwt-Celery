# Generated by Django 5.1 on 2024-08-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtauth', '0004_userdata_is_verified_userdata_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField()),
            ],
        ),
    ]
