from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.support_dashboard, name='dashboard'),
    
    # Emergency Contacts
    path('emergency/', views.emergency_contacts, name='emergency'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/update/', views.contact_update, name='contact_update'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    # Support Tickets
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:pk>/reply/', views.ticket_reply, name='ticket_reply'),
    
    # FAQ
    path('faq/', views.faq_list, name='faq'),
    path('faq/<int:pk>/vote/', views.faq_vote, name='faq_vote'),
    
    # Resources
    path('resources/', views.resource_list, name='resources'),
    
    # Chat
    path('chat/', views.chat_view, name='chat'),
    path('chat/send/', views.send_message, name='send_message'),
]
