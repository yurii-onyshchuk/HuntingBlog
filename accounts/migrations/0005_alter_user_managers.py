# Generated by Django 4.1.3 on 2023-03-09 09:37

import accounts.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_email_alter_user_photo_alter_user_slug_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.managers.CustomUserManager()),
            ],
        ),
    ]
