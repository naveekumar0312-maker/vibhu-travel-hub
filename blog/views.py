from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    query = request.GET.get('q', '').strip()
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(short_description__icontains=query) |
            Q(content__icontains=query)
        )
    
    posts_list = list(posts)
    featured_post = posts_list[0] if len(posts_list) > 0 else None
    other_posts = posts_list[1:] if len(posts_list) > 1 else []
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:5]

    context = {
        'posts': posts,
        'featured_post': featured_post,
        'other_posts': other_posts,
        'recent_posts': recent_posts,
        'search_query': query,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    context = {
        'post': post,
    }
    return render(request, 'blog/blog_detail.html', context)
