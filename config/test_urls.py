from django.shortcuts import render
from django.urls import path
import markdown
import os
from django.conf import settings

def home_view(request):
    """Professional home page for Baby Moms Care Clinic"""
    return render(request, 'home.html')

def test_view(request):
    """Simple test view for debugging"""
    return render(request, 'home.html')

def tutorial_view(request):
    """Tutorial page displaying user guide"""
    tutorial_path = os.path.join(settings.BASE_DIR, 'USER_TUTORIAL.md')
    tutorial_content = ''
    
    try:
        with open(tutorial_path, 'r', encoding='utf-8') as f:
            tutorial_md = f.read()
            tutorial_content = markdown.markdown(tutorial_md, extensions=['extra', 'codehilite', 'toc'])
    except FileNotFoundError:
        tutorial_content = '<p>Tutorial content not found.</p>'
    
    return render(request, 'tutorial.html', {'tutorial_content': tutorial_content})

urlpatterns = [
    path('', home_view, name='home'),
    path('test/', test_view, name='test'),
    path('tutorial/', tutorial_view, name='tutorial'),
]
