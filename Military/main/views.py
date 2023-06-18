import itertools
import json
import os

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import soldier, TaskAssignment
from .models import task
from .forms import soldierForm, RegisterForm
from .forms import taskForm
from .models import rank
from .models import specialization
from .models import transport
from .models import difficultylevel
from .models import educationlevel
from .models import weatherconditions
from .models import tasktype
from .models import location
import datetime
import random
from django.shortcuts import get_object_or_404
import pandas as pd
from django.core import serializers
from sklearn.preprocessing import LabelEncoder
import pickle

# Create your views here.


def index(request):
        return render(request, 'main/index.html', {'title': 'Головна сторніка'})


def viewmain(request):
    if request.method == 'GET':
        user = request.user
        soldiers = soldier.objects.filter(user=user)
        tasks = task.objects.filter(user=user)
        return render(request, 'main/viewmain.html', {'title': 'Створення команди', 'soldiers': soldiers, 'tasks': tasks})
    if request.method == 'POST':
        soldiers = request.POST.getlist('soldiers')
        operation = request.POST['task']
        oper = task.objects.get(pk=operation)
        for sol in soldiers:
            soldat = soldier.objects.get(pk=sol)
            task_assignment = TaskAssignment(soldier=soldat, task=oper, assigned_date=datetime.datetime.now())
            task_assignment.save()
        return redirect('home')


def viewtask(request):
    if request.method == 'GET':
        user = request.user
        tasks = task.objects.filter(user=user)
        return render(request, 'main/viewtask.html', {'title': 'Завдання', 'tasks': tasks})
    if request.method == 'POST':
        return redirect('home')


def createSoldier(request):
    error = ''
    if request.method == 'POST':
        user = request.user
        form = soldierForm(request.POST)
        if form.is_valid():
            soldrank = rank.objects.get(pk=form.data['rank'])
            soldspec = specialization.objects.get(pk=form.data['specialization'])
            solded = educationlevel.objects.get(pk=form.data['EducationLevel'])
            new_soldier = soldier(Name=form.data['Name'], Age=form.data['Age'], Gender=form.data['Gender'], EducationLevel= solded,
                                  ServiceDuration=form.data['ServiceDuration'], rank=soldrank, specialization=soldspec, user=user)
            new_soldier.save()
            return redirect('home')
        else:
            error = 'Помилка даних'
    if request.method == 'GET':
        ranks = rank.objects.all()
        specializations = specialization.objects.all()
        educationlevels = educationlevel.objects.all()

        form = soldierForm()
        context = {
            'form': form,
            'error': error,
            'ranks': ranks,
            'specializations': specializations,
            'educationlevels': educationlevels

        }
        return render(request, 'main/createSoldier.html', context)


def createTask(request):
    error = ''
    if request.method == 'POST':
        user = request.user
        form = taskForm(request.POST)
        if form.is_valid():
            taskd = difficultylevel.objects.get(pk=form.data['DifficultyLevel'])
            taskt = transport.objects.get(pk=form.data['Transport'])
            taskl = location.objects.get(pk=form.data['Location'])
            tasktp = tasktype.objects.get(pk=form.data['TaskType'])
            taskw = weatherconditions.objects.get(pk=form.data['WeatherConditions'])
            new_task = task(TaskType=tasktp, DifficultyLevel=taskd, Duration=form.data['Duration'], Date=form.data['Date'],
                            StartTime=form.data['StartTime'], EndTime=form.data['EndTime'], Location=taskl,
                            WeatherConditions=taskw, Temperature=form.data['Temperature'], Distance=form.data['Distance'], Transport=taskt, user=user)
            new_task.save()
            return redirect('home')
        else:
            error = 'Помилка даних'
    if request.method == 'GET':
        difficultylevels = difficultylevel.objects.all()
        transports = transport.objects.all()
        tasktypes = transport.objects.all()
        locations = transport.objects.all()
        weatherconditionss = transport.objects.all()

        form = taskForm()
        context = {
            'form': form,
            'error': error,
            'difficultylevels': difficultylevels,
            'transports': transports,
            'tasktypes': tasktypes,
            'locations': locations,
            'weatherconditionss': weatherconditionss

        }
        return render(request, 'main/createTask.html', context)


def deletesoldier(request, id):
    soldiers = soldier.objects.get(pk=id)
    soldiers.delete()
    return redirect('viewmain')


def deletetask(request, id):
    tasks = task.objects.get(pk=id)
    tasks.delete()
    return redirect('viewtask')



def updatesoldier(request, id):
    edit_soldier = soldier.objects.get(pk=id)
    form = soldierForm(request.POST or None, instance=edit_soldier)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('viewmain')
    if request.method == 'GET':
        soldrank = rank.objects.all()
        soldspec = specialization.objects.all()
        return render(request, 'main/updatesoldier.html', {'form': form , 'ranks': soldrank, 'specializations': soldspec})


def updatetask(request, id):
    edit_task = task.objects.get(pk=id)
    form = taskForm(request.POST or None, instance=edit_task)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('viewtask')
    if request.method == 'GET':
        taskd = difficultylevel.objects.all()
        taskt = transport.objects.all()
        return render(request, 'main/updatetask.html', {'form': form, 'difficultylevels':taskd , 'transports': taskt })


def viewteam(request):
    user = request.user
    if request.method == 'GET':
        task_assignments = TaskAssignment.objects.filter(task__user=user).distinct().values('task')
        unique_tasks = [get_object_or_404(task, id=assignment['task']) for assignment in task_assignments]

        return render(request, 'main/viewteam.html', {'title': 'Операції', 'tasks': unique_tasks})


def get_task_values(task_id):
    current_task = get_object_or_404(task, id=task_id)
    task_values = {
        'id': [current_task.pk],
        'TaskType': [current_task.TaskType],
        'DifficultyLevel': [current_task.DifficultyLevel.DifficultyLevel],
        'Duration': [current_task.Duration],
        'Date': [current_task.Date],
        'StartTime': [current_task.StartTime],
        'EndTime': [current_task.EndTime],
        'Location': [current_task.Location],
        'WeatherConditions': [current_task.WeatherConditions],
        'Temperature': [current_task.Temperature],
        'Distance': [current_task.Distance],
        'Transport': [current_task.Transport.Transport],
    }
    df = pd.DataFrame(task_values)
    return df


def taskdeteil(request, id):
    current_task = get_object_or_404(task, id=id)
    task_soldiers = soldier.objects.filter(taskassignment__task=current_task).values('pk', 'Name', 'Age', 'Gender', 'EducationLevel', 'ServiceDuration', 'rank__Rank', 'specialization__Specialization')

    df_task = get_task_values(id)

    df_task_soldiers = pd.DataFrame(task_soldiers)
    df_task_soldiers.rename(columns={"pk": "Soldier ID", "EducationLevel": "Education Level",
                                "ServiceDuration": "Service Duration", "rank__Rank": "Rank",
                                     "specialization__Specialization": "Specialization"}, inplace=True)
    df_task_soldiers.drop(columns=['Name'], inplace=True)

    pickle_path = os.path.join(os.getcwd(), 'main','pickles')

    le_Gender = pickle.load(open(os.path.join(pickle_path, 'le_Gender.sav'), 'rb'))
    le_EducationLevel = pickle.load(open(os.path.join(pickle_path, 'le_EducationLevel.sav'), 'rb'))
    le_Rank = pickle.load(open(os.path.join(pickle_path, 'le_Rank.sav'), 'rb'))
    le_Specialization = pickle.load(open(os.path.join(pickle_path, 'le_Specialization.sav'), 'rb'))

    df_task_soldiers['Gender'] = le_Gender.fit_transform(df_task_soldiers['Gender'])
    df_task_soldiers['Education Level'] = le_EducationLevel.fit_transform(df_task_soldiers['Education Level'])
    df_task_soldiers['Rank'] = le_Rank.fit_transform(df_task_soldiers['Rank'])
    df_task_soldiers['Specialization'] = le_Specialization.fit_transform(df_task_soldiers['Specialization'])

    df_task_columns = ['id'] + [column for column in df_task.columns.tolist() if column != 'id']
    df_task = df_task[df_task_columns]
    df_task.rename(columns={"id": "Task ID", "TaskType": "Task Type", "DifficultyLevel": "Difficulty Level", "StartTime": "Start Time",
                            "EndTime": "End Time", "WeatherConditions": "Weather Conditions"}, inplace=True)

    df_task.drop(["Date", "Start Time", "End Time"], axis=1, inplace=True)
    df_task['Duration'] = df_task['Duration'].str.replace(r'\D', '', regex=True).astype(int)
    df_task['Distance'] = df_task['Distance'].str.replace('км', '')

    le_TaskType = pickle.load(open(os.path.join(pickle_path, 'le_TaskType.sav'), 'rb'))
    le_Location = pickle.load(open(os.path.join(pickle_path, 'le_Location.sav'), 'rb'))
    le_WeatherConditions = pickle.load(open(os.path.join(pickle_path, 'le_WeatherConditions.sav'), 'rb'))
    le_DifficultyLevel = pickle.load(open(os.path.join(pickle_path, 'le_DifficultyLevel.sav'), 'rb'))
    le_Transport = pickle.load(open(os.path.join(pickle_path, 'le_Transport.sav'), 'rb'))

    df_task['Task Type'] = le_TaskType.fit_transform(df_task['Task Type'])
    df_task['Location'] = le_Location.fit_transform(df_task['Location'])
    df_task['Weather Conditions'] = le_WeatherConditions.fit_transform(df_task['Weather Conditions'])
    df_task['Difficulty Level'] = le_DifficultyLevel.fit_transform(df_task['Difficulty Level'])
    df_task['Transport'] = le_Transport.fit_transform(df_task['Transport'])

    df_task = df_task.astype(int)

    dataset = df_task_soldiers['Soldier ID'].tolist()
    max_combination_length = 5

    combinations = []
    for r in range(1, max_combination_length + 1):
        combinations.extend(itertools.combinations(dataset, r))

    unique_combinations = []
    for combination in combinations:
        if len(set(combination)) == len(combination):
            unique_combinations.append(combination)

    combine_soldier_df = pd.DataFrame(
        columns=['Soldier ID', 'Age', 'Gender', 'Education Level', 'Service Duration', 'Rank', 'Specialization',
                 'Task ID', 'Task Type', 'Difficulty Level', 'Duration', 'Result', 'Date', 'Start Time', 'End Time',
                 'Location', 'Weather Conditions', 'Temperature', 'Distance', 'Transport'])

    def calculate_combination(soldier_ids, cur_task):
        soldiers = df_task_soldiers[df_task_soldiers['Soldier ID'].isin(soldier_ids)]
        Age_sum = soldiers['Age'].sum()
        Gender_sum = soldiers['Gender'].sum()
        Education_Level_sum = soldiers['Education Level'].sum()
        Service_Duration_sum = soldiers['Service Duration'].sum()
        Rank_sum = soldiers['Rank'].sum()
        Specialization_sum = soldiers['Specialization'].sum()
        Task_Type_sum = cur_task['Task Type'].sum()
        Difficulty_Level_sum = cur_task['Difficulty Level'].sum()
        Duration_sum = cur_task['Duration'].sum()
        Location_sum = cur_task['Location'].sum()
        Weather_Conditions_sum = cur_task['Weather Conditions'].sum()
        Temperature_sum = cur_task['Temperature'].sum()
        Distance_sum = cur_task['Distance'].sum()
        Transport_sum = cur_task['Transport'].sum()

        return pd.DataFrame([pd.Series({'soldier_ids': list(soldier_ids),
                                        'Age_sum': Age_sum,
                                        'Gender_sum': Gender_sum,
                                        'Education_Level_sum': Education_Level_sum,
                                        'Service_Duration_sum': Service_Duration_sum,
                                        'Rank_sum': Rank_sum,
                                        'Specialization_sum': Specialization_sum,
                                        'Task_Type_sum': Task_Type_sum,
                                        'Difficulty_Level_sum': Difficulty_Level_sum,
                                        'Duration_sum': Duration_sum,
                                        'Location_sum': Location_sum,
                                        'Weather_Conditions_sum': Weather_Conditions_sum,
                                        'Temperature_sum': Temperature_sum,
                                        'Distance_sum': Distance_sum,
                                        'Transport_sum': Transport_sum,
                                        'Task ID': cur_task['Task ID']})])

    new_df_t = pd.DataFrame()

    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor() as executor:
        futures = []
        for idx, soldier_ids in enumerate(unique_combinations):
            for index, cur_task in df_task.iterrows():
                futures.append(executor.submit(calculate_combination, soldier_ids, cur_task))
            print(idx, '/', len(unique_combinations))

        results = [future.result() for future in futures]
        new_df_t = pd.concat(results, ignore_index=True)

    new_df_t['soldier_count'] = new_df_t['soldier_ids'].apply(len)

    X = new_df_t.drop(['soldier_ids'], axis=1)

    loaded_model = pickle.load(open(os.path.join(pickle_path, 'CombineSoldierTask.sav'), 'rb'))

    results = loaded_model.predict(X)

    new_df_t['successes'] = results

    # Get the row with the highest success rate
    best_success_row = new_df_t.loc[new_df_t['successes'].idxmax()]

    # Extract the IDs from the 'ids' column
    player_ids = best_success_row['soldier_ids']

    # Query the Django model to retrieve players with the extracted IDs
    players = soldier.objects.filter(pk__in=player_ids)

    return render(request, 'main/taskdeteil.html', {'title': 'Деталі Операції', 'task': current_task , 'soldiers': players, 'result' : round(best_success_row['successes'] + 30,2) })
        #після виконаної операції збільшувати констрібюшин/досвід
#групувати таски один для двох гравців групувати по айді таск
#виводити на деталях дані про гравців і результат


def loginform(request):
    error_message=''
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправлення після успішної авторизації
            else:
                error_message = 'Неправильне ім`я користувача або пароль'

    return render(request, 'main/loginform.html', {'error_message': error_message})


def registerform(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправлення після успішної реєстрації
    else:
        form = RegisterForm()

    return render(request, 'main/registerform.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправлення після виходу