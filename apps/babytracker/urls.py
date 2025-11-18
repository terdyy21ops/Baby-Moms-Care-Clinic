from django.urls import path
from . import views

app_name = 'babytracker'

urlpatterns = [
    path('', views.baby_list, name='list'),
    path('create/', views.baby_create, name='create'),
    path('<int:pk>/', views.baby_detail, name='detail'),
    path('<int:pk>/update/', views.baby_update, name='update'),
    path('<int:pk>/delete/', views.baby_delete, name='delete'),
    
    # Growth Records
    path('<int:baby_pk>/growth/create/', views.growth_record_create, name='growth_create'),
    path('<int:baby_pk>/growth/<int:pk>/update/', views.growth_record_update, name='growth_update'),
    path('<int:baby_pk>/growth/<int:pk>/delete/', views.growth_record_delete, name='growth_delete'),
    
    # Feeding Records
    path('<int:baby_pk>/feeding/create/', views.feeding_record_create, name='feeding_create'),
    path('<int:baby_pk>/feeding/<int:pk>/update/', views.feeding_record_update, name='feeding_update'),
    path('<int:baby_pk>/feeding/<int:pk>/delete/', views.feeding_record_delete, name='feeding_delete'),
    
    # Sleep Records
    path('<int:baby_pk>/sleep/create/', views.sleep_record_create, name='sleep_create'),
    path('<int:baby_pk>/sleep/<int:pk>/update/', views.sleep_record_update, name='sleep_update'),
    path('<int:baby_pk>/sleep/<int:pk>/delete/', views.sleep_record_delete, name='sleep_delete'),
    
    # Diaper Records
    path('<int:baby_pk>/diaper/create/', views.diaper_record_create, name='diaper_create'),
    path('<int:baby_pk>/diaper/<int:pk>/update/', views.diaper_record_update, name='diaper_update'),
    path('<int:baby_pk>/diaper/<int:pk>/delete/', views.diaper_record_delete, name='diaper_delete'),
    
    # Vaccination Records
    path('<int:baby_pk>/vaccination/create/', views.vaccination_record_create, name='vaccination_create'),
    path('<int:baby_pk>/vaccination/<int:pk>/update/', views.vaccination_record_update, name='vaccination_update'),
    path('<int:baby_pk>/vaccination/<int:pk>/delete/', views.vaccination_record_delete, name='vaccination_delete'),
    
    # Milestone Records
    path('<int:baby_pk>/milestone/create/', views.milestone_record_create, name='milestone_create'),
    path('<int:baby_pk>/milestone/<int:pk>/update/', views.milestone_record_update, name='milestone_update'),
    path('<int:baby_pk>/milestone/<int:pk>/delete/', views.milestone_record_delete, name='milestone_delete'),
    
    # Charts and Analytics
    path('<int:baby_pk>/growth-chart/', views.growth_chart, name='growth_chart'),
    path('<int:baby_pk>/feeding-chart/', views.feeding_chart, name='feeding_chart'),
    path('<int:baby_pk>/sleep-chart/', views.sleep_chart, name='sleep_chart'),
]
