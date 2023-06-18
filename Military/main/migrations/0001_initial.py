# Generated by Django 4.2.1 on 2023-06-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='squad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Назва операції')),
                ('success', models.FloatField(max_length=10, verbose_name='Успішність операції')),
            ],
        ),
    ]