from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='list'),
    path('create/', views.article_create, name='create'),
    path('category/<slug:category_slug>/', views.article_by_category, name='by_category'),
    path('<slug:slug>/', views.article_detail, name='detail'),
    path('<slug:slug>/update/', views.article_update, name='update'),
    path('<slug:slug>/delete/', views.article_delete, name='delete'),
    path('<slug:slug>/like/', views.article_like, name='like'),
    path('<slug:slug>/bookmark/', views.article_bookmark, name='bookmark'),
    
    # Comments
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # User's articles and bookmarks
    path('my/articles/', views.my_articles, name='my_articles'),
    path('my/bookmarks/', views.my_bookmarks, name='my_bookmarks'),
]
