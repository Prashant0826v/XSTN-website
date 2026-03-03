"""
XSTN Backend — Comprehensive Test Suite
Tests all 8 form API submissions, database storage, model verification,
user authentication, and core form endpoints.
"""
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.forms.models import (
    ContactForm, InquiryForm, InternshipApplication, DeveloperApplication,
    JoinApplication, ConsultationRequest, NewsletterSubscription, Testimonial
)
from core.models import (
    JoinCommunity, ContactMessage, ProposalForm,
    DeveloperApplication as CoreDeveloperApplication,
    ConsultationRequest as CoreConsultationRequest,
    NewsletterSubscription as CoreNewsletterSubscription,
    Testimonial as CoreTestimonial,
    InternshipApplication as CoreInternshipApplication,
)

User = get_user_model()


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: MODEL TESTS — Verify all models can be created and stored in DB
# ══════════════════════════════════════════════════════════════════════════════

class ContactFormModelTest(TestCase):
    """Test ContactForm model creation and verification"""

    def test_create_contact_form(self):
        form = ContactForm.objects.create(
            name='Test User', email='test@example.com',
            phone='+911234567890', subject='Testing',
            message='This is a test message.'
        )
        self.assertEqual(ContactForm.objects.count(), 1)
        self.assertEqual(form.name, 'Test User')
        self.assertFalse(form.is_read)
        self.assertFalse(form.is_verified)
        self.assertIsNotNone(form.created_at)

    def test_contact_form_str(self):
        form = ContactForm.objects.create(
            name='Prashant', email='p@test.com',
            subject='Hello', message='Test'
        )
        self.assertEqual(str(form), 'Prashant - Hello')

    def test_contact_form_verification_token(self):
        form = ContactForm.objects.create(
            name='User', email='u@test.com',
            subject='Sub', message='Msg'
        )
        token = form.generate_verification_token()
        self.assertIsNotNone(token)
        self.assertTrue(form.is_verification_token_valid())

    def test_contact_form_verify_email(self):
        form = ContactForm.objects.create(
            name='User', email='u@test.com',
            subject='Sub', message='Msg'
        )
        form.generate_verification_token()
        result = form.verify_email()
        self.assertTrue(result)
        self.assertTrue(form.is_verified)
        self.assertIsNotNone(form.verified_at)

    def test_phone_optional(self):
        form = ContactForm.objects.create(
            name='User', email='u@test.com',
            subject='Sub', message='Msg'
        )
        self.assertIsNone(form.phone)


class InquiryFormModelTest(TestCase):
    """Test InquiryForm model"""

    def test_create_inquiry(self):
        form = InquiryForm.objects.create(
            name='Client', email='client@corp.com',
            company='Corp Ltd', project_type='Web App',
            budget_range='50k-100k', timeline='3 months',
            message='Need a website.'
        )
        self.assertEqual(InquiryForm.objects.count(), 1)
        self.assertEqual(str(form), 'Client - Web App')

    def test_optional_fields(self):
        form = InquiryForm.objects.create(
            name='X', email='x@test.com',
            project_type='Mobile App', message='Need app'
        )
        self.assertIsNone(form.company)
        self.assertIsNone(form.budget_range)
        self.assertIsNone(form.timeline)


class InternshipApplicationModelTest(TestCase):
    """Test InternshipApplication model"""

    def test_create_application(self):
        app = InternshipApplication.objects.create(
            full_name='Student One', email='student@uni.edu',
            phone='+919999999999', university='IIT Delhi',
            skills='Python, Django, React'
        )
        self.assertEqual(app.status, 'pending')
        self.assertFalse(app.is_read)

    def test_status_update(self):
        app = InternshipApplication.objects.create(
            full_name='Student', email='s@uni.edu',
            phone='+91111', university='MIT', skills='JS'
        )
        for s in ['reviewed', 'selected', 'rejected']:
            app.status = s
            app.save()
            app.refresh_from_db()
            self.assertEqual(app.status, s)

    def test_verification_flow(self):
        app = InternshipApplication.objects.create(
            full_name='S', email='s@t.com', phone='1', university='U', skills='X'
        )
        token = app.generate_verification_token()
        self.assertTrue(app.is_verification_token_valid())
        self.assertTrue(app.verify_email())
        self.assertTrue(app.is_verified)


class DeveloperApplicationModelTest(TestCase):
    """Test DeveloperApplication model"""

    def test_create_developer_application(self):
        app = DeveloperApplication.objects.create(
            full_name='Dev User', email='dev@test.com',
            phone='+91222', role_interested='Backend Developer',
            experience_level='intermediate',
            skills='Python, Django, PostgreSQL',
            message='I want to join XSTN.'
        )
        self.assertEqual(app.status, 'pending')
        self.assertEqual(app.experience_level, 'intermediate')

    def test_experience_levels(self):
        for level in ['beginner', 'intermediate', 'advanced', 'expert']:
            app = DeveloperApplication.objects.create(
                full_name='D', email=f'{level}@test.com', phone='1',
                role_interested='Dev', experience_level=level,
                skills='X', message='Y'
            )
            self.assertEqual(app.experience_level, level)


class JoinApplicationModelTest(TestCase):
    """Test JoinApplication model"""

    def test_create_join_application(self):
        app = JoinApplication.objects.create(
            full_name='Joiner', email='join@test.com',
            role_interested='Content Writer',
            why_join='I love XSTN!'
        )
        self.assertEqual(app.status, 'pending')
        self.assertEqual(str(app), 'Joiner - Content Writer')


class ConsultationRequestModelTest(TestCase):
    """Test ConsultationRequest model"""

    def test_create_consultation(self):
        req = ConsultationRequest.objects.create(
            full_name='Business Owner', email='biz@corp.com',
            phone='+91333', consultation_type='website',
            requirement='Need a company website'
        )
        self.assertEqual(req.status, 'pending')

    def test_consultation_types(self):
        for ct in ['website', 'app', 'ui_ux', 'business', 'other']:
            req = ConsultationRequest.objects.create(
                full_name='T', email=f'{ct}@t.com',
                consultation_type=ct, requirement='R'
            )
            self.assertEqual(req.consultation_type, ct)


class NewsletterSubscriptionModelTest(TestCase):
    """Test NewsletterSubscription model"""

    def test_create_subscription(self):
        sub = NewsletterSubscription.objects.create(email='news@test.com')
        self.assertTrue(sub.is_active)
        self.assertEqual(str(sub), 'news@test.com')

    def test_unique_email(self):
        NewsletterSubscription.objects.create(email='unique@test.com')
        with self.assertRaises(Exception):
            NewsletterSubscription.objects.create(email='unique@test.com')

    def test_unsubscribe(self):
        sub = NewsletterSubscription.objects.create(email='unsub@test.com')
        sub.is_active = False
        sub.save()
        sub.refresh_from_db()
        self.assertFalse(sub.is_active)


class TestimonialModelTest(TestCase):
    """Test Testimonial model"""

    def test_create_testimonial(self):
        t = Testimonial.objects.create(
            name='Happy Client', company='Corp', email='happy@test.com',
            rating=5, message='Excellent work!'
        )
        self.assertFalse(t.is_approved)
        self.assertEqual(str(t), 'Happy Client - 5★')

    def test_rating_range(self):
        for r in range(1, 6):
            t = Testimonial.objects.create(
                name=f'C{r}', email=f'c{r}@t.com',
                rating=r, message='Good'
            )
            self.assertEqual(t.rating, r)


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: API TESTS — Submit all 8 forms via REST API and verify response + DB
# ══════════════════════════════════════════════════════════════════════════════

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ContactFormAPITest(APITestCase):
    """Test POST /api/forms/contact-forms/"""

    def test_submit_contact_form(self):
        data = {
            'name': 'API Test User',
            'email': 'apitest@example.com',
            'phone': '+911234567890',
            'subject': 'API Test Subject',
            'message': 'Testing form submission via API.'
        }
        response = self.client.post('/api/forms/contact-forms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactForm.objects.count(), 1)
        self.assertIn('message', response.data)

    def test_submit_contact_form_missing_required(self):
        data = {'name': 'Incomplete'}  # missing email, subject, message
        response = self.client.post('/api/forms/contact-forms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContactForm.objects.count(), 0)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class InquiryFormAPITest(APITestCase):
    """Test POST /api/forms/inquiry-forms/"""

    def test_submit_inquiry_form(self):
        data = {
            'name': 'Inquiry User',
            'email': 'inquiry@example.com',
            'company': 'TestCorp',
            'project_type': 'Web Application',
            'budget_range': '1L-5L',
            'timeline': '6 months',
            'message': 'We need a web app built.'
        }
        response = self.client.post('/api/forms/inquiry-forms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InquiryForm.objects.count(), 1)

    def test_submit_inquiry_minimal(self):
        data = {
            'name': 'Min User', 'email': 'min@test.com',
            'project_type': 'Mobile App', 'message': 'Need app'
        }
        response = self.client.post('/api/forms/inquiry-forms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class InternshipApplicationAPITest(APITestCase):
    """Test POST /api/forms/internship-applications/"""

    def test_submit_internship_application(self):
        data = {
            'full_name': 'Intern Student',
            'email': 'intern@university.edu',
            'phone': '+919876543210',
            'university': 'IIT Bombay',
            'skills': 'Python, Machine Learning, Django',
            'experience': '2 personal projects',
        }
        response = self.client.post('/api/forms/internship-applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InternshipApplication.objects.count(), 1)
        app = InternshipApplication.objects.first()
        self.assertEqual(app.full_name, 'Intern Student')
        self.assertEqual(app.status, 'pending')

    def test_submit_internship_missing_fields(self):
        data = {'full_name': 'Only Name'}
        response = self.client.post('/api/forms/internship-applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class DeveloperApplicationAPITest(APITestCase):
    """Test POST /api/forms/developer-applications/"""

    def test_submit_developer_application(self):
        data = {
            'full_name': 'Developer John',
            'email': 'devjohn@example.com',
            'phone': '+911111111111',
            'role_interested': 'Full Stack Developer',
            'experience_level': 'advanced',
            'skills': 'React, Node.js, Python, Docker',
            'portfolio_url': 'https://devjohn.com',
            'github_url': 'https://github.com/devjohn',
            'message': 'I want to contribute to XSTN projects.'
        }
        response = self.client.post('/api/forms/developer-applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DeveloperApplication.objects.count(), 1)

    def test_submit_developer_minimal(self):
        data = {
            'full_name': 'Dev', 'email': 'dev@t.com', 'phone': '1',
            'role_interested': 'Backend', 'skills': 'Python',
            'message': 'Hi'
        }
        response = self.client.post('/api/forms/developer-applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class JoinApplicationAPITest(APITestCase):
    """Test POST /api/forms/join-applications/"""

    def test_submit_join_application(self):
        data = {
            'full_name': 'Join User',
            'email': 'joinuser@example.com',
            'role_interested': 'Community Manager',
            'why_join': 'I believe in the XSTN mission!'
        }
        response = self.client.post('/api/forms/join-applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JoinApplication.objects.count(), 1)

    def test_submit_join_missing_fields(self):
        data = {'full_name': 'Only Name'}
        response = self.client.post('/api/forms/join-applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ConsultationRequestAPITest(APITestCase):
    """Test POST /api/forms/consultation-requests/"""

    def test_submit_consultation_request(self):
        data = {
            'full_name': 'Business Owner',
            'email': 'business@corp.com',
            'phone': '+912222222222',
            'consultation_type': 'website',
            'requirement': 'Need a company website with blog and CMS.'
        }
        response = self.client.post('/api/forms/consultation-requests/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsultationRequest.objects.count(), 1)

    def test_submit_consultation_all_types(self):
        for i, ct in enumerate(['website', 'app', 'ui_ux', 'business', 'other']):
            data = {
                'full_name': f'User {i}', 'email': f'u{i}@t.com',
                'consultation_type': ct, 'requirement': f'Need {ct}'
            }
            response = self.client.post('/api/forms/consultation-requests/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsultationRequest.objects.count(), 5)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class NewsletterSubscriptionAPITest(APITestCase):
    """Test POST /api/forms/newsletter-subscriptions/"""

    def test_subscribe_newsletter(self):
        data = {'email': 'subscriber@example.com'}
        response = self.client.post('/api/forms/newsletter-subscriptions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)
        sub = NewsletterSubscription.objects.first()
        self.assertTrue(sub.is_active)

    def test_duplicate_subscription(self):
        data = {'email': 'dup@example.com'}
        self.client.post('/api/forms/newsletter-subscriptions/', data, format='json')
        response = self.client.post('/api/forms/newsletter-subscriptions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestimonialAPITest(APITestCase):
    """Test POST /api/forms/testimonials/"""

    def test_submit_testimonial(self):
        data = {
            'name': 'Happy Client',
            'company': 'Success Corp',
            'email': 'happy@corp.com',
            'rating': 5,
            'message': 'XSTN delivered an amazing product! Highly recommended.'
        }
        response = self.client.post('/api/forms/testimonials/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Testimonial.objects.count(), 1)
        t = Testimonial.objects.first()
        self.assertFalse(t.is_approved)  # needs admin approval

    def test_submit_testimonial_all_ratings(self):
        for r in range(1, 6):
            data = {
                'name': f'Client{r}', 'email': f'c{r}@t.com',
                'rating': r, 'message': f'{r} stars'
            }
            response = self.client.post('/api/forms/testimonials/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Testimonial.objects.count(), 5)


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: CORE API TESTS — Test the core app form endpoints
# ══════════════════════════════════════════════════════════════════════════════

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreJoinCommunityAPITest(APITestCase):
    """Test POST /api/join/"""

    def test_submit_join_community(self):
        data = {
            'full_name': 'Community Member',
            'email': 'member@xstn.com',
            'role': 'Volunteer',
            'message': 'I want to join the community!'
        }
        response = self.client.post('/api/join/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submit_missing_fields(self):
        data = {'full_name': 'Incomplete'}
        response = self.client.post('/api/join/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreContactAPITest(APITestCase):
    """Test POST /api/contact/"""

    def test_submit_contact(self):
        data = {
            'full_name': 'Contact Person',
            'email': 'contact@test.com',
            'subject': 'General Inquiry',
            'message': 'I have a question about your services.'
        }
        response = self.client.post('/api/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreInternshipAPITest(APITestCase):
    """Test POST /api/internship/"""

    def test_submit_internship(self):
        data = {
            'full_name': 'Intern Applicant',
            'email': 'intern@college.edu',
            'phone': '+919999888877',
            'position': 'frontend',
            'experience': 'Built 5 React projects',
            'cover_letter': 'I am passionate about frontend development...'
        }
        response = self.client.post('/api/internship/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreProposalAPITest(APITestCase):
    """Test POST /api/proposal/"""

    def test_submit_proposal(self):
        data = {
            'name': 'Proposal Client',
            'email': 'proposal@corp.com',
            'company': 'BigCorp',
            'project_type': 'E-commerce Platform',
            'budget_range': '5L-10L',
            'timeline': '4 months',
            'message': 'We need a full e-commerce solution.'
        }
        response = self.client.post('/api/proposal/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreDeveloperAPITest(APITestCase):
    """Test POST /api/developer-application/"""

    def test_submit_developer(self):
        data = {
            'full_name': 'Core Dev',
            'email': 'coredev@test.com',
            'phone': '+91444',
            'role_interested': 'DevOps Engineer',
            'experience_level': 'advanced',
            'skills': 'AWS, Docker, Kubernetes',
            'message': 'I have 5 years of DevOps experience.'
        }
        response = self.client.post('/api/developer-application/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreConsultationAPITest(APITestCase):
    """Test POST /api/consultation/"""

    def test_submit_consultation(self):
        data = {
            'full_name': 'Consultant Client',
            'email': 'consult@biz.com',
            'phone': '+91555',
            'consultation_type': 'business',
            'requirement': 'Need advice on tech stack for startup.'
        }
        response = self.client.post('/api/consultation/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreNewsletterAPITest(APITestCase):
    """Test POST /api/newsletter/"""

    def test_subscribe(self):
        data = {'email': 'newsletter@test.com'}
        response = self.client.post('/api/newsletter/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CoreTestimonialAPITest(APITestCase):
    """Test POST /api/testimonial/"""

    def test_submit_testimonial(self):
        data = {
            'name': 'Core Client',
            'email': 'core@test.com',
            'rating': 4,
            'message': 'Great service by XSTN!'
        }
        response = self.client.post('/api/testimonial/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# ══════════════════════════════════════════════════════════════════════════════
# PART 4: USER AUTH TESTS
# ══════════════════════════════════════════════════════════════════════════════

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class UserRegistrationAPITest(APITestCase):
    """Test user registration via /api/users/register/"""

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@xstn.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'newuser')
        self.assertFalse(user.is_verified)

    def test_register_password_mismatch(self):
        data = {
            'username': 'user2', 'email': 'user2@test.com',
            'password': 'StrongPass123!', 'confirm_password': 'DifferentPass!'
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        data = {
            'username': 'user3', 'email': 'dup@test.com',
            'password': 'StrongPass123!', 'confirm_password': 'StrongPass123!'
        }
        self.client.post('/api/users/register/', data, format='json')
        data['username'] = 'user4'
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserModelTest(TestCase):
    """Test custom User model features"""

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser', email='test@xstn.com',
            password='TestPass123!'
        )
        self.assertFalse(user.is_verified)
        self.assertEqual(user.failed_login_attempts, 0)

    def test_verification_code_generation(self):
        user = User.objects.create_user(
            username='verifyuser', email='verify@xstn.com',
            password='TestPass123!'
        )
        code = user.generate_verification_code()
        user.save()
        self.assertIsNotNone(code)
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_account_locking(self):
        user = User.objects.create_user(
            username='lockuser', email='lock@xstn.com',
            password='TestPass123!'
        )
        self.assertFalse(user.is_account_locked())
        for _ in range(5):
            user.record_failed_login()
        self.assertTrue(user.is_account_locked())

    def test_reset_failed_attempts(self):
        user = User.objects.create_user(
            username='resetuser', email='reset@xstn.com',
            password='TestPass123!'
        )
        for _ in range(3):
            user.record_failed_login()
        self.assertEqual(user.failed_login_attempts, 3)
        user.reset_failed_login_attempts()
        self.assertEqual(user.failed_login_attempts, 0)

    def test_email_verification(self):
        user = User.objects.create_user(
            username='emailuser', email='email@xstn.com',
            password='TestPass123!'
        )
        user.generate_verification_code()
        user.save()
        user.verify_email()
        self.assertTrue(user.is_verified)
        self.assertIsNotNone(user.email_verified_at)
        self.assertIsNone(user.email_verification_code)


# ══════════════════════════════════════════════════════════════════════════════
# PART 5: HEALTH CHECK & GENERAL ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

class HealthCheckTest(APITestCase):
    """Test health check endpoint"""

    def test_health_check(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')

    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forms_api_contact_endpoint(self):
        """Verify the forms API endpoints are reachable"""
        response = self.client.get('/api/forms/contact-forms/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])
