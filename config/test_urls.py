from django.shortcuts import render
from django.urls import path

def home_view(request):
    """Professional home page for Baby Moms Care Clinic"""
    return render(request, 'home.html')

def test_view(request):
    """Simple test view for debugging"""
    return render(request, 'home.html')

urlpatterns = [
    path('', home_view, name='home'),
    path('test/', test_view, name='test'),
]
