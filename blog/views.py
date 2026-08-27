from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import BlogPost, CATEGORY_CHOICES

CATEGORIES_LIST = ['All'] + [c[0] for c in CATEGORY_CHOICES]

def blog_list(request):
    all_published = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', 'All').strip()
    
    posts = all_published
    
    if selected_category and selected_category != 'All':
        posts = posts.filter(category__iexact=selected_category)
        
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(short_description__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        )
    
    # Identify Featured Post (if no active filter/search)
    featured_post = None
    if not query and selected_category == 'All':
        featured_post = all_published.filter(is_featured=True).first()
        if not featured_post:
            featured_post = all_published.first()
            
    # Filter out featured_post from general listing grid if featured section is shown
    grid_posts = posts
    if featured_post and not query and selected_category == 'All':
        grid_posts = posts.exclude(id=featured_post.id)
        
    recent_posts = all_published[:5]

    context = {
        'posts': grid_posts,
        'featured_post': featured_post,
        'categories': CATEGORIES_LIST,
        'selected_category': selected_category,
        'search_query': query,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Related posts in same category, fallback to latest
    related_posts = list(BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(id=post.id).order_by('-published_date')[:3])
    
    if len(related_posts) < 3:
        needed = 3 - len(related_posts)
        existing_ids = [p.id for p in related_posts] + [post.id]
        fallback_posts = list(BlogPost.objects.filter(
            is_published=True
        ).exclude(id__in=existing_ids).order_by('-published_date')[:needed])
        related_posts.extend(fallback_posts)
        
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:5]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
        'categories': CATEGORIES_LIST,
    }
    return render(request, 'blog/blog_detail.html', context)

