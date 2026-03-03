import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def create_or_reset_admin(username, email, password):
    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.is_verified = True  # Crucial for mandatory verification settings
    user.email_verified_at = timezone.now()
    user.failed_login_attempts = 0
    user.locked_until = None
    user.save()
    status = "created" if created else "updated"
    print(f"✓ Superuser '{username}' {status} successfully!")
    return user

# Main Admin
create_or_reset_admin('admin', 'prashant.iron2@gmail.com', 'admin@123')

# Fallback Admin (just in case)
create_or_reset_admin('owner', 'prashant.iron1@gmail.com', 'Owner@123')

print("\nLogin Credentials:")
print("1. Username: admin | Password: admin@123")
print("2. Username: owner | Password: Owner@123")
print("\nTry logging in with both if one fails.")
