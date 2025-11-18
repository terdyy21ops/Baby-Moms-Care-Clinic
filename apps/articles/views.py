from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, ArticleCategory, ArticleLike, ArticleBookmark, ArticleComment


def article_list(request):
    articles = Article.objects.filter(status='published').order_by('-published_at')
    categories = ArticleCategory.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    
    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'articles/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    
    # Increment view count
    article.views_count += 1
    article.save(update_fields=['views_count'])
    
    # Get comments
    comments = ArticleComment.objects.filter(article=article, is_approved=True, parent=None)
    
    # Check if user has liked or bookmarked
    user_liked = False
    user_bookmarked = False
    if request.user.is_authenticated:
        user_liked = ArticleLike.objects.filter(article=article, user=request.user).exists()
        user_bookmarked = ArticleBookmark.objects.filter(article=article, user=request.user).exists()
    
    return render(request, 'articles/detail.html', {
        'article': article,
        'comments': comments,
        'user_liked': user_liked,
        'user_bookmarked': user_bookmarked,
    })


@login_required
def article_create(request):
    # Placeholder view
    messages.info(request, 'Article creation feature coming soon!')
    return redirect('articles:list')


@login_required
def article_update(request, slug):
    # Placeholder view
    messages.info(request, 'Article editing feature coming soon!')
    return redirect('articles:detail', slug=slug)


@login_required
def article_delete(request, slug):
    # Placeholder view
    messages.info(request, 'Article deletion feature coming soon!')
    return redirect('articles:list')


def article_by_category(request, category_slug):
    category = get_object_or_404(ArticleCategory, slug=category_slug, is_active=True)
    articles = Article.objects.filter(category=category, status='published').order_by('-published_at')
    
    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'articles/category.html', {
        'category': category,
        'page_obj': page_obj,
    })


@login_required
def article_like(request, slug):
    if request.method == 'POST':
        article = get_object_or_404(Article, slug=slug)
        like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        # Update like count
        article.likes_count = ArticleLike.objects.filter(article=article).count()
        article.save(update_fields=['likes_count'])
        
        return JsonResponse({'liked': liked, 'likes_count': article.likes_count})
    
    return JsonResponse({'error': 'Invalid request'})


@login_required
def article_bookmark(request, slug):
    if request.method == 'POST':
        article = get_object_or_404(Article, slug=slug)
        bookmark, created = ArticleBookmark.objects.get_or_create(article=article, user=request.user)
        
        if not created:
            bookmark.delete()
            bookmarked = False
        else:
            bookmarked = True
        
        return JsonResponse({'bookmarked': bookmarked})
    
    return JsonResponse({'error': 'Invalid request'})


@login_required
def add_comment(request, slug):
    # Placeholder view
    messages.info(request, 'Comment feature coming soon!')
    return redirect('articles:detail', slug=slug)


@login_required
def delete_comment(request, comment_id):
    # Placeholder view
    messages.info(request, 'Comment deletion feature coming soon!')
    return redirect('articles:list')


@login_required
def my_articles(request):
    # Placeholder view
    messages.info(request, 'My articles feature coming soon!')
    return redirect('articles:list')


@login_required
def my_bookmarks(request):
    # Placeholder view
    messages.info(request, 'My bookmarks feature coming soon!')
    return redirect('articles:list')
