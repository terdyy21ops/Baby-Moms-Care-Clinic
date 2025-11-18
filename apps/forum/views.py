from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def category_list(request):
    # Placeholder view
    return render(request, 'forum/category_list.html', {
        'categories': [],
    })


def post_list(request, category_slug):
    # Placeholder view
    return render(request, 'forum/post_list.html', {
        'posts': [],
        'category_slug': category_slug,
    })


@login_required
def post_create(request, category_slug):
    messages.info(request, 'Forum posting feature coming soon!')
    return redirect('forum:category_list')


def post_detail(request, slug):
    # Placeholder view
    return render(request, 'forum/post_detail.html', {
        'post': None,
    })


@login_required
def post_update(request, slug):
    messages.info(request, 'Post editing feature coming soon!')
    return redirect('forum:category_list')


@login_required
def post_delete(request, slug):
    messages.info(request, 'Post deletion feature coming soon!')
    return redirect('forum:category_list')


@login_required
def post_like(request, slug):
    messages.info(request, 'Post liking feature coming soon!')
    return redirect('forum:category_list')


@login_required
def post_bookmark(request, slug):
    messages.info(request, 'Post bookmarking feature coming soon!')
    return redirect('forum:category_list')


@login_required
def post_report(request, slug):
    messages.info(request, 'Post reporting feature coming soon!')
    return redirect('forum:category_list')


@login_required
def add_comment(request, slug):
    messages.info(request, 'Comment feature coming soon!')
    return redirect('forum:category_list')


@login_required
def update_comment(request, comment_id):
    messages.info(request, 'Comment editing feature coming soon!')
    return redirect('forum:category_list')


@login_required
def delete_comment(request, comment_id):
    messages.info(request, 'Comment deletion feature coming soon!')
    return redirect('forum:category_list')


@login_required
def comment_like(request, comment_id):
    messages.info(request, 'Comment liking feature coming soon!')
    return redirect('forum:category_list')


@login_required
def my_posts(request):
    messages.info(request, 'My posts feature coming soon!')
    return redirect('forum:category_list')


@login_required
def my_bookmarks(request):
    messages.info(request, 'My bookmarks feature coming soon!')
    return redirect('forum:category_list')


def search_posts(request):
    messages.info(request, 'Search feature coming soon!')
    return redirect('forum:category_list')
