# Generated by Django 4.2.1 on 2023-06-07 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_task_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.task')),
            ],
        ),
        migrations.CreateModel(
            name='SquadSoldiers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='soldier',
            name='tasks',
        ),
        migrations.DeleteModel(
            name='TaskAssignment',
        ),
        migrations.AddField(
            model_name='squadsoldiers',
            name='soldier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.soldier'),
        ),
        migrations.AddField(
            model_name='squadsoldiers',
            name='squad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.squad'),
        ),
        migrations.AddField(
            model_name='soldier',
            name='squads',
            field=models.ManyToManyField(through='main.SquadSoldiers', to='main.squad'),
        ),
    ]
