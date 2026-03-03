"""
XSTN Real Email Delivery Test
Submits forms to the LIVE Django server and verifies real emails are sent.
Run the server first:  python manage.py runserver
Then run this:         python test_real_email.py
"""
import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "prashant.iron1@gmail.com"

# All form submissions to test
TESTS = [
    {
        "name": "1. Contact Form (Core)",
        "url": f"{BASE_URL}/api/contact/",
        "data": {
            "full_name": "Test User",
            "email": ADMIN_EMAIL,
            "subject": "Real Email Test - Contact",
            "message": "Testing real email delivery from Contact form."
        }
    },
    {
        "name": "2. Join Community (Core)",
        "url": f"{BASE_URL}/api/join/",
        "data": {
            "full_name": "Test Joiner",
            "email": ADMIN_EMAIL,
            "role": "Volunteer",
            "message": "Testing real email delivery from Join form."
        }
    },
    {
        "name": "3. Proposal (Core)",
        "url": f"{BASE_URL}/api/proposal/",
        "data": {
            "name": "Test Proposer",
            "email": ADMIN_EMAIL,
            "company": "TestCorp",
            "project_type": "Web App",
            "budget_range": "1L-5L",
            "timeline": "3 months",
            "message": "Testing real email delivery from Proposal form."
        }
    },
    {
        "name": "4. Internship (Core)",
        "url": f"{BASE_URL}/api/internship/",
        "data": {
            "full_name": "Test Intern",
            "email": ADMIN_EMAIL,
            "phone": "+919999999999",
            "position": "frontend",
            "experience": "2 projects",
            "cover_letter": "Testing real email delivery from Internship form."
        }
    },
    {
        "name": "5. Developer Application (Core)",
        "url": f"{BASE_URL}/api/developer-application/",
        "data": {
            "full_name": "Test Developer",
            "email": ADMIN_EMAIL,
            "phone": "+911111111111",
            "role_interested": "Backend Developer",
            "experience_level": "advanced",
            "skills": "Python, Django",
            "message": "Testing real email delivery from Developer form."
        }
    },
    {
        "name": "6. Consultation (Core)",
        "url": f"{BASE_URL}/api/consultation/",
        "data": {
            "full_name": "Test Consultant",
            "email": ADMIN_EMAIL,
            "phone": "+912222222222",
            "consultation_type": "website",
            "requirement": "Testing real email delivery from Consultation form."
        }
    },
    {
        "name": "7. Newsletter (Core)",
        "url": f"{BASE_URL}/api/newsletter/",
        "data": {
            "email": ADMIN_EMAIL
        }
    },
    {
        "name": "8. Testimonial (Core)",
        "url": f"{BASE_URL}/api/testimonial/",
        "data": {
            "name": "Test Client",
            "email": ADMIN_EMAIL,
            "rating": 5,
            "message": "Testing real email delivery from Testimonial form."
        }
    },
]

def run_tests():
    print("=" * 60)
    print("  XSTN Real Email Delivery Test")
    print(f"  Server: {BASE_URL}")
    print(f"  Admin Email: {ADMIN_EMAIL}")
    print("=" * 60)

    # Check if server is running
    try:
        r = requests.get(f"{BASE_URL}/health/", timeout=5)
        print(f"\n  Server status: {r.json().get('status', 'unknown')}")
    except requests.ConnectionError:
        print("\n  ERROR: Server is not running!")
        print("  Start it with: python manage.py runserver")
        sys.exit(1)

    print(f"\n  Running {len(TESTS)} form submission tests...\n")
    print("-" * 60)

    passed = 0
    failed = 0

    for test in TESTS:
        try:
            response = requests.post(
                test["url"],
                json=test["data"],
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code == 201:
                print(f"  PASS  {test['name']}")
                print(f"        -> Status: {response.status_code}")
                resp_data = response.json()
                if 'message' in resp_data:
                    print(f"        -> Response: {resp_data['message'][:80]}")
                passed += 1
            else:
                print(f"  FAIL  {test['name']}")
                print(f"        -> Status: {response.status_code}")
                print(f"        -> Response: {response.text[:200]}")
                failed += 1

        except Exception as e:
            print(f"  ERROR {test['name']}")
            print(f"        -> {str(e)[:100]}")
            failed += 1

        # Small delay to avoid overwhelming SMTP
        time.sleep(1)

    print("-" * 60)
    print(f"\n  Results: {passed} passed, {failed} failed, {len(TESTS)} total")
    print(f"\n  Check your inbox at: {ADMIN_EMAIL}")
    print(f"  You should receive confirmation + admin notification emails")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
