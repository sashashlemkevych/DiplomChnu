# Generated by Django 4.2.1 on 2023-06-06 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_user_loginform_username'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LoginForm',
            new_name='Login',
        ),
    ]