import os
# pyrefly: ignore [missing-import]
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

# pyrefly: ignore [missing-import]
from django.db import connection

cursor = connection.cursor()
tables_to_drop = [
    'blog_blogpost_tags',
    'blog_blogpost',
    'blog_tag',
    'blog_category'
]

for table in tables_to_drop:
    try:
        cursor.execute(f"DROP TABLE {table}")
        print(f"Dropped {table}")
    except Exception as e:
        print(f"Failed to drop {table}: {e}")

print("Done dropping tables")
