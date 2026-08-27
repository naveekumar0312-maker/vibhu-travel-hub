# pyrefly: ignore [missing-import]
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        exclude = ['author', 'published_date']
        labels = {
            'title': 'Blog Title',
            'category': 'Category',
            'short_description': 'Short Description / Excerpt',
            'featured_image': 'Featured Image',
            'content': 'Blog Content',
            'reading_time': 'Estimated Reading Time',
            'is_featured': 'Mark as Featured Article',
            'is_published': 'Published Status',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Best Weekend Getaways from Coimbatore'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary or excerpt of the article...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'id': 'blog-content-editor', 'placeholder': 'Enter HTML content here...'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'reading_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5 min read'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
