# Backend Testing Guide

## Overview

This testing suite provides comprehensive test coverage for the XSTN Django backend including:
- **Model Tests**: Validation of database models
- **Serializer Tests**: API data serialization/deserialization
- **API View Tests**: Endpoint functionality and permissions
- **Integration Tests**: Full workflow testing

## Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Pytest configuration
├── test_user_model.py       # User model tests (11 tests)
├── test_form_models.py      # Form model tests (20 tests)
├── test_serializers.py      # Serializer tests (15 tests)
└── test_api_views.py        # API endpoint tests (18 tests)
```

**Total: 64 comprehensive test cases**

## Running Tests

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Module
```bash
# User model tests
python manage.py test tests.test_user_model

# Form model tests
python manage.py test tests.test_form_models

# Serializer tests
python manage.py test tests.test_serializers

# API view tests
python manage.py test tests.test_api_views
```

### Run Specific Test Class
```bash
python manage.py test tests.test_user_model.UserModelTests
```

### Run Specific Test Method
```bash
python manage.py test tests.test_user_model.UserModelTests.test_user_creation
```

### Run with Coverage Report
```bash
# First install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test tests

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html
```

### Run with Verbose Output
```bash
python manage.py test tests -v 2
```

## Test Categories

### 1. User Model Tests (test_user_model.py)
- User creation and validation
- Email uniqueness
- Authentication code generation
- Password hashing
- Timestamp tracking
- Account locking mechanism
- Superuser creation

### 2. Form Model Tests (test_form_models.py)

**ContactForm Tests:**
- Form creation and field validation
- Timestamps
- Read status management
- Optional fields

**InquiryForm Tests:**
- Inquiry creation
- Optional company and budget fields
- String representation
- Timestamps

**InternshipApplication Tests:**
- Application creation
- Status choices validation
- Optional portfolio fields
- Status updates

**DeveloperApplication Tests:**
- Application creation
- Experience level validation
- Optional GitHub/Portfolio URLs

### 3. Serializer Tests (test_serializers.py)
- Serialization and deserialization
- Field validation
- Required vs optional fields
- Email and status validation
- Read-only field enforcement

### 4. API View Tests (test_api_views.py)
- Contact form endpoint
- Inquiry form endpoint
- Internship application endpoint
- Developer application endpoint
- Admin access controls
- Status management

## Expected Test Results

When running all tests, you should see output similar to:

```
Ran 64 tests in 2.345s

OK
```

## Test Data

### Contact Form Test Data
```python
{
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '+1234567890',
    'subject': 'Website Inquiry',
    'message': 'I would like to know more...'
}
```

### Internship Application Test Data
```python
{
    'full_name': 'Bob Johnson',
    'email': 'bob@example.com',
    'phone': '+9876543210',
    'university': 'MIT',
    'skills': 'Python, Django, React',
    'experience': 'Built 3 projects'
}
```

### Developer Application Test Data
```python
{
    'full_name': 'Charlie Brown',
    'email': 'charlie@example.com',
    'phone': '+5555555555',
    'skills': 'JavaScript, React, Node.js',
    'experience_level': 'intermediate',
    'portfolio_url': 'https://portfolio.example.com',
    'github_url': 'https://github.com/charlie'
}
```

## Adding New Tests

When adding new models or features:

1. Create test file in `tests/` directory
2. Follow naming convention: `test_<feature>.py`
3. Use descriptive test class and method names
4. Include docstrings for each test
5. Run tests: `python manage.py test`
6. Check coverage: `coverage report`

## Continuous Integration

To integrate with CI/CD:

```yaml
# GitHub Actions example
- name: Run Django Tests
  run: |
    python manage.py test tests
    coverage run --source='.' manage.py test tests
    coverage report --fail-under=80
```

## Troubleshooting

### Import Errors
Make sure Django app is properly configured in `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'apps.users',
    'apps.forms',
]
```

### Database Errors
Tests use a temporary test database. If issues persist:
```bash
python manage.py flush  # Clear database
python manage.py migrate  # Run migrations
python manage.py test tests
```

### Fixture Issues
Use `setUp()` method for test data instead of fixtures for simpler tests.

## Best Practices

✅ **DO:**
- Write test for each model method
- Test edge cases and validation errors  
- Use descriptive test names
- Keep tests focused and independent
- Mock external API calls
- Test permission levels

❌ **DON'T:**
- Write tests that depend on other tests
- Use hardcoded data across tests
- Skip test output analysis
- Test framework code (Django's built-in)
- Create unnecessary test data

## Performance

For faster test execution:
```bash
python manage.py test tests --parallel auto
```

## Test Metrics

- **Total Tests**: 64
- **Models Covered**: 5 (User, ContactForm, InquiryForm, InternshipApplication, DeveloperApplication)
- **Expected Coverage**: 85%+

