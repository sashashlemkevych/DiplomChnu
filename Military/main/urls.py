from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('viewmain', views.viewmain, name='viewmain'),
    path('createSoldier', views.createSoldier, name='createSoldier'),
    path('createTask', views.createTask, name='createTask'),
    path('viewteam', views.viewteam, name='viewteam'),
    path('viewtask', views.viewtask, name='viewtask'),
    path('taskdeteil/<int:id>/', views.taskdeteil, name='taskdeteil'),
    path('loginform', views.loginform, name='loginform'),
    path('registerform', views.registerform, name='registerform'),
    path('logout', views.logout_view, name='logout'),
    path('updatesoldier/<int:id>/', views.updatesoldier, name='updatesoldier'),
    path('deletesoldier/<int:id>/', views.deletesoldier, name='deletesoldier'),
    path('updatetask/<int:id>/', views.updatetask, name='updatetask'),
    path('deletetask/<int:id>/', views.deletetask, name='deletetask'),
]