import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

# Check for existing admin user
admin_user = User.objects.filter(username='admin').first()

if admin_user:
    print(f"Found existing admin user: {admin_user.username}")
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"✓ Password updated to: admin123")
else:
    print("Creating new admin user...")
    admin_user = User.objects.create_superuser(
        username='admin',
        email='prashant.iron2@gmail.com',
        password='admin123'
    )
    print(f"✓ Created superuser:")
    print(f"  Username: admin")
    print(f"  Password: admin123")
    print(f"  Email: prashant.iron2@gmail.com")

print(f"\nLogin credentials for admin panel:")
print(f"  URL: http://localhost:8000/admin/")
print(f"  Username: admin")
print(f"  Password: admin123")

