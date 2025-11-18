from django.urls import path
from . import views

app_name = 'pregnancy'

urlpatterns = [
    path('', views.pregnancy_dashboard, name='dashboard'),
    path('list/', views.pregnancy_list, name='list'),
    path('create/', views.pregnancy_create, name='create'),
    path('<int:pk>/', views.pregnancy_detail, name='detail'),
    path('<int:pk>/update/', views.pregnancy_update, name='update'),
    
    # Weekly logs
    path('<int:pregnancy_pk>/weekly-log/create/', views.weekly_log_create, name='weekly_log_create'),
    path('<int:pregnancy_pk>/weekly-log/<int:log_pk>/update/', views.weekly_log_update, name='weekly_log_update'),
    path('<int:pregnancy_pk>/weekly-log/<int:log_pk>/delete/', views.weekly_log_delete, name='weekly_log_delete'),
    
    # Milestones
    path('<int:pregnancy_pk>/milestone/create/', views.milestone_create, name='milestone_create'),
    path('<int:pregnancy_pk>/milestone/<int:milestone_pk>/update/', views.milestone_update, name='milestone_update'),
    path('<int:pregnancy_pk>/milestone/<int:milestone_pk>/delete/', views.milestone_delete, name='milestone_delete'),
    
    # Reminders
    path('<int:pregnancy_pk>/reminder/create/', views.reminder_create, name='reminder_create'),
    path('<int:pregnancy_pk>/reminder/<int:reminder_pk>/update/', views.reminder_update, name='reminder_update'),
    path('<int:pregnancy_pk>/reminder/<int:reminder_pk>/delete/', views.reminder_delete, name='reminder_delete'),
]
