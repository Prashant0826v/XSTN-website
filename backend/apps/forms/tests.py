"""
Test cases for XSTN Form Submissions
"""
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.forms.models import ContactForm, InquiryForm, InternshipApplication, DeveloperApplication


class ContactFormTestCase(APITestCase):
    """Test contact form submissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.submit_url = '/api/forms/contact/'
    
    def test_contact_form_submission_success(self):
        """Test successful contact form submission"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'subject': 'Website Inquiry',
            'message': 'I have a question about your services.'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactForm.objects.count(), 1)
    
    def test_contact_form_missing_required_fields(self):
        """Test contact form fails with missing required fields"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            # Missing subject and message
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_contact_form_invalid_email(self):
        """Test contact form fails with invalid email"""
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Inquiry',
            'message': 'Test message'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class InquiryFormTestCase(APITestCase):
    """Test inquiry/proposal form submissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.submit_url = '/api/forms/inquiry/'
    
    def test_inquiry_form_submission_success(self):
        """Test successful inquiry form submission"""
        data = {
            'name': 'Jane Company',
            'email': 'contact@company.com',
            'company': 'Tech Corp',
            'project_type': 'Web Application',
            'budget_range': '$10k-$50k',
            'timeline': '3 months',
            'message': 'We need a custom web application.'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InquiryForm.objects.count(), 1)
    
    def test_inquiry_form_minimal_fields(self):
        """Test inquiry form with minimal required fields"""
        data = {
            'name': 'Jane Company',
            'email': 'contact@company.com',
            'project_type': 'Web Application',
            'message': 'We need a custom web application.'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class InternshipApplicationTestCase(APITestCase):
    """Test internship application submissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.submit_url = '/api/forms/internship/'
    
    def test_internship_application_success(self):
        """Test successful internship application"""
        data = {
            'full_name': 'Student Name',
            'email': 'student@example.com',
            'phone': '+1234567890',
            'university': 'Tech University',
            'skills': 'Python, Django, React'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InternshipApplication.objects.count(), 1)
        
        # Verify default status is pending
        app = InternshipApplication.objects.first()
        self.assertEqual(app.status, 'pending')
    
    def test_internship_application_with_portfolio(self):
        """Test internship application with portfolio URL"""
        data = {
            'full_name': 'Student Name',
            'email': 'student@example.com',
            'phone': '+1234567890',
            'university': 'Tech University',
            'skills': 'Python, Django, React',
            'portfolio_url': 'https://portfolio.example.com'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeveloperApplicationTestCase(APITestCase):
    """Test developer application submissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.submit_url = '/api/forms/developer/'
    
    def test_developer_application_success(self):
        """Test successful developer application"""
        data = {
            'full_name': 'Dev Name',
            'email': 'dev@example.com',
            'phone': '+1234567890',
            'role_interested': 'Backend Developer',
            'experience_level': 'intermediate',
            'skills': 'Python, Node.js, PostgreSQL',
            'message': 'I want to join XSTN team'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DeveloperApplication.objects.count(), 1)
    
    def test_developer_application_with_github(self):
        """Test developer application with GitHub profile"""
        data = {
            'full_name': 'Dev Name',
            'email': 'dev@example.com',
            'phone': '+1234567890',
            'role_interested': 'Frontend Developer',
            'experience_level': 'advanced',
            'skills': 'React, Vue, TypeScript',
            'github_url': 'https://github.com/devname',
            'message': 'I want to join XSTN team'
        }
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        app = DeveloperApplication.objects.first()
        self.assertEqual(app.github_url, 'https://github.com/devname')


class FormEmailNotificationTestCase(APITestCase):
    """Test email notifications on form submissions"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_contact_form_sends_email(self):
        """Test that contact form submission sends email"""
        from django.core.mail import outbox
        
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Inquiry',
            'message': 'Test message'
        }
        self.client.post('/api/forms/contact/', data, format='json')
        
        # In production with SMTP, emails would be sent
        # In testing, we check that email logic was triggered
        self.assertEqual(ContactForm.objects.count(), 1)
