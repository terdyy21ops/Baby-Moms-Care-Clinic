from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/', views.post_list, name='post_list'),
    path('category/<slug:category_slug>/create/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/update/', views.post_update, name='post_update'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
    path('post/<slug:slug>/bookmark/', views.post_bookmark, name='post_bookmark'),
    path('post/<slug:slug>/report/', views.post_report, name='post_report'),
    
    # Comments
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/update/', views.update_comment, name='update_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/like/', views.comment_like, name='comment_like'),
    
    # User's posts and bookmarks
    path('my/posts/', views.my_posts, name='my_posts'),
    path('my/bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    
    # Search
    path('search/', views.search_posts, name='search'),
]
