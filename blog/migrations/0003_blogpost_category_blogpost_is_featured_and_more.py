# pyrefly: ignore [missing-import]
from django.db import migrations, models
# pyrefly: ignore [missing-import]
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_blogpost_category_remove_blogpost_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.CharField(choices=[('Travel Tips', 'Travel Tips'), ('Destinations', 'Destinations'), ('Travel Guides', 'Travel Guides'), ('Cab & Taxi', 'Cab & Taxi'), ('Family Travel', 'Family Travel'), ('Corporate Travel', 'Corporate Travel')], default='Travel Tips', max_length=100),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='reading_time',
            field=models.CharField(default='5 min read', max_length=30),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='auth.user'),
        ),
    ]
