# Generated by Django 5.0.6 on 2024-09-08 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userinfos_userprofile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]
