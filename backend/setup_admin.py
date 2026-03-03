import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

username = 'admin'
email = 'prashant.iron2@gmail.com'
password = 'admin@123'

# Delete existing admin if exists
User.objects.filter(username=username).delete()

# Create superuser
user = User.objects.create_superuser(username=username, email=email, password=password)
print(f"✓ Superuser created successfully!")
print(f"  Username: {username}")
print(f"  Email: {email}")
print(f"  Password: {password}")
print(f"  Admin panel: http://localhost:8000/admin")
