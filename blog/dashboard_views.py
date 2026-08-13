# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm

@login_required
def dashboard_blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'dashboard/blog/blog_list.html', {'posts': posts})

@login_required
def dashboard_blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_published = True
            post.save()
            form.save_m2m()
            messages.success(request, 'Blog post created successfully.')
            return redirect('dashboard_blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'dashboard/blog/blog_form.html', {'form': form, 'title': 'Add Blog Post'})

@login_required
def dashboard_blog_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('dashboard_blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'dashboard/blog/blog_form.html', {'form': form, 'title': 'Edit Blog Post'})

@login_required
def dashboard_blog_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    messages.success(request, 'Blog post deleted successfully.')
    return redirect('dashboard_blog_list')

@login_required
def dashboard_blog_toggle(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.is_published = not post.is_published
    post.save()
    messages.success(request, f"Blog post {'published' if post.is_published else 'unpublished'}.")
    return redirect('dashboard_blog_list')
