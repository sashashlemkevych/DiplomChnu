from django.contrib.auth.models import User
from django import forms
from .models import soldier
from .models import task
from django.forms import ModelForm, TextInput, NumberInput, DateInput, DateTimeInput, TimeInput, Select


class soldierForm(ModelForm):
    class Meta:
        model = soldier
        fields = ["Name", "Age", "Gender", "EducationLevel", "ServiceDuration", "rank", "specialization"]
        widgets = {
            "Name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Позивний'
            }),
            "Age": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вік'
            }),
            "Gender": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Стать'
            }),
            "EducationLevel": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Рівень освіти'
            }),
            "ServiceDuration": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тривалість служби'
            }),
            "rank": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Ранг'
            }),
            "specialization": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Спеціалізація'
            }),
        }


class taskForm(ModelForm):
    class Meta:
        model = task
        fields = ["TaskType", "DifficultyLevel", "Duration", "Date", "StartTime", "EndTime", "Location", "WeatherConditions", "Temperature", "Distance", "Transport"]
        widgets = {
            "TaskType": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Тип задачі'
            }),
            "DifficultyLevel": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Рівень складності'
            }),
            "Duration": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тривалість'
            }),
            "Date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата виконання'
            }),
            "StartTime": TimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Час початку'
            }),
            "EndTime": TimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Час закінчення'
            }),
            "Location": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Місце виконання'
            }),
            "WeatherConditions": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Погодні умови'
            }),
            "Temperature": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Температура'
            }),
            "Distance": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Відстань'
            }),
            "Transport": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Транспорт'
            }),
        }


class RegisterForm(ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email']
