# pyrefly: ignore [missing-import]
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'short_description', 'featured_image', 'content', 'is_published']
        labels = {
            'title': 'Blog Title',
            'short_description': 'Short Description',
            'featured_image': 'Blog Image',
            'content': 'Blog Content',
            'is_published': 'Published',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Best Tourist Places to Visit in Tamil Nadu'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the blog...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'id': 'blog-content-editor', 'placeholder': 'Enter HTML content here...'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content:
            import bleach
            # Allow only the safe tags requested by the user
            allowed_tags = [
                'h2', 'h3', 'h4', 'p', 'strong', 'b', 'em', 
                'ul', 'ol', 'li', 'blockquote', 'a', 'br', 'img'
            ]
            allowed_attributes = {
                'a': ['href', 'title', 'target'],
                'img': ['src', 'alt', 'width', 'height']
            }
            # Clean the content
            content = bleach.clean(
                content,
                tags=allowed_tags,
                attributes=allowed_attributes,
                strip=True
            )
        return content
