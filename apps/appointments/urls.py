from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='list'),
    path('create/', views.appointment_create, name='create'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:pk>/update/', views.appointment_update, name='update'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='cancel'),
    path('calendar/', views.calendar_view, name='calendar'),
    
    # Doctor availability URLs
    path('availability/', views.doctor_availability, name='availability'),
    path('availability/create/', views.availability_create, name='availability_create'),
    path('availability/<int:pk>/update/', views.availability_update, name='availability_update'),
    path('availability/<int:pk>/delete/', views.availability_delete, name='availability_delete'),
    path('check-availability/', views.check_availability, name='check_availability'),
]
