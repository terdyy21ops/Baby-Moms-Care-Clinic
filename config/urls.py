"""
URL configuration for Baby Moms Care project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('config.test_urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('pregnancy/', include('apps.pregnancy.urls')),
    path('baby/', include('apps.babytracker.urls')),
    path('articles/', include('apps.articles.urls')),
    path('forum/', include('apps.forum.urls')),
    path('support/', include('apps.support.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
