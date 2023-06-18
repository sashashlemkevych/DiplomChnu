from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class difficultylevel(models.Model):
    DifficultyLevel = models.CharField('Складність', max_length=30)

    def __str__(self):
        return self.DifficultyLevel


class transport(models.Model):
    Transport = models.CharField('Транспорт', max_length=225)

    def __str__(self):
        return self.Transport


class tasktype(models.Model):
    TaskType = models.CharField('Тип задачі', max_length=225)

    def __str__(self):
        return self.TaskType


class location(models.Model):
    Location = models.CharField('Місце виконання', max_length=225)

    def __str__(self):
        return self.Location


class weatherconditions(models.Model):
    WeatherConditions = models.CharField('Погодні умови', max_length=225)

    def __str__(self):
        return self.WeatherConditions


class task(models.Model):
    TaskType = models.ForeignKey(tasktype, on_delete=models.CASCADE)
    DifficultyLevel = models.ForeignKey(difficultylevel, on_delete=models.CASCADE)
    Duration = models.CharField('Тривалість', max_length=30)
    Date = models.DateField('Дата виконання', max_length=30)
    StartTime = models.TimeField('Час початку', max_length=30)
    EndTime = models.TimeField('Час закінчення', max_length=30)
    Location = models.ForeignKey(location, on_delete=models.CASCADE)
    WeatherConditions = models.ForeignKey(weatherconditions, on_delete=models.CASCADE)
    Temperature = models.IntegerField('Температура')
    Distance = models.CharField('Відстань', max_length=30)
    Transport = models.ForeignKey(transport, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.TaskType.TaskType


class rank(models.Model):
    Rank = models.CharField('Звання', max_length=30)

    def __str__(self):
        return self.Rank


class specialization(models.Model):
    Specialization = models.CharField('Спеціалізація', max_length=30)

    def __str__(self):
        return self.Specialization


class educationlevel(models.Model):
    EducationLevel = models.CharField('Рівень освіти', max_length=30)

    def __str__(self):
        return self.EducationLevel


class soldier(models.Model):
    Name = models.CharField('Позивний', max_length=30)
    Age = models.IntegerField('Вік')
    Gender = models.CharField('Стать', max_length=30)
    EducationLevel = models.ForeignKey(educationlevel, on_delete=models.CASCADE)
    ServiceDuration = models.IntegerField('Тривалість служби')
    rank = models.ForeignKey(rank, on_delete=models.CASCADE)
    specialization = models.ForeignKey(specialization, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(task, through='TaskAssignment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class TaskAssignment(models.Model):
    soldier = models.ForeignKey(soldier, on_delete=models.CASCADE)
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    assigned_date = models.DateField()

    def __str__(self):
        return f'{self.soldier} - {self.task}'



