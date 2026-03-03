import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

# Credentials
username = 'admin'
email = 'prashant.iron2@gmail.com'
password = 'admin@123'  # Note: Use a more secure password in production

# Check if superuser already exists
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✓ Superuser '{username}' created successfully!")
else:
    # Optional: Update the password if it already exists to ensure login works
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"✓ Superuser '{username}' password updated successfully!")

print(f"  Username: {username}")
print(f"  Password: {password}")
