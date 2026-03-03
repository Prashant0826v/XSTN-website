"""
Test cases for XSTN Authentication System
"""
import json
from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class UserRegistrationTestCase(APITestCase):
    """Test user registration and authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/users/register/'
        
    def test_user_registration_success(self):
        """Test successful user registration"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'confirm_password': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
    
    def test_user_registration_password_mismatch(self):
        """Test registration fails with mismatched passwords"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'confirm_password': 'WrongPass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_weak_password(self):
        """Test registration fails with weak password"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'weak',  # Too short, no uppercase, no digit
            'confirm_password': 'weak',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_duplicate_username(self):
        """Test registration fails with duplicate username"""
        # Create first user
        User.objects.create_user(
            username='testuser',
            email='first@example.com',
            password='TestPass123'
        )
        
        # Try to create second user with same username
        data = {
            'username': 'testuser',
            'email': 'second@example.com',
            'password': 'TestPass123',
            'confirm_password': 'TestPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):
    """Test user login functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/token/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
    
    def test_user_login_success(self):
        """Test successful user login"""
        data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_login_wrong_password(self):
        """Test login fails with wrong password"""
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_login_nonexistent_user(self):
        """Test login fails for nonexistent user"""
        data = {
            'username': 'nonexistent',
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmailVerificationTestCase(APITestCase):
    """Test email verification functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.verify_url = '/api/users/verify_email/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        # Generate and save verification code
        self.user.generate_verification_code()
        self.user.save()
    
    def test_email_verification_success(self):
        """Test successful email verification"""
        code = self.user.email_verification_code
        data = {
            'email': 'test@example.com',
            'code': code
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify user is marked as verified
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.email_verified_at)
    
    def test_email_verification_wrong_code(self):
        """Test verification fails with wrong code"""
        data = {
            'email': 'test@example.com',
            'code': 'WRONG000'
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_email_verification_nonexistent_email(self):
        """Test verification fails for nonexistent email"""
        data = {
            'email': 'nonexistent@example.com',
            'code': '123456'
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PasswordResetTestCase(APITestCase):
    """Test password reset functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.reset_request_url = '/api/users/request_password_reset/'
        self.reset_url = '/api/users/reset_password/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPass123'
        )
    
    def test_password_reset_request_success(self):
        """Test successful password reset request"""
        data = {'email': 'test@example.com'}
        response = self.client.post(self.reset_request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify reset token is generated
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.password_reset_token)
    
    def test_password_reset_confirm_success(self):
        """Test successful password reset confirmation"""
        # Generate reset token
        self.user.generate_password_reset_token()
        self.user.save()
        token = self.user.password_reset_token
        
        data = {
            'token': token,
            'password': 'NewPass456',
            'confirm_password': 'NewPass456'
        }
        response = self.client.post(self.reset_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password is changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456'))


class AccountLockoutTestCase(APITestCase):
    """Test account lockout after failed attempts"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/token/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
    
    def test_account_lockout_after_failed_attempts(self):
        """Test account is locked after 5 failed login attempts"""
        # Simulate failed login attempts by calling record_failed_login()
        for i in range(5):
            self.user.record_failed_login()
        
        # Verify account is locked
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.locked_until)
        self.assertTrue(self.user.is_account_locked())


class ChangePasswordTestCase(APITestCase):
    """Test password change functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.change_password_url = '/api/users/change_password/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_change_password_success(self):
        """Test successful password change"""
        data = {
            'old_password': 'OldPass123',
            'new_password': 'NewPass456',
            'confirm_new_password': 'NewPass456'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password is changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456'))
    
    def test_change_password_wrong_old_password(self):
        """Test password change fails with wrong old password"""
        data = {
            'old_password': 'WrongOldPass',
            'new_password': 'NewPass456',
            'confirm_new_password': 'NewPass456'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
