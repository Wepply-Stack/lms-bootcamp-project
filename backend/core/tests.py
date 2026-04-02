from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from core.models import Course


class APIContractTests(APITestCase):
    LOGIN_URL = "/api/auth/login"
    LOGOUT_URL = "/api/auth/logout"
    DASHBOARD_URL = "/api/admin/dashboard"
    COURSES_URL = "/api/courses"
    USERS_URL = "/api/users"

    def setUp(self):
        self.superuser = User.objects.create_user(
            username="admin",
            email="admin@email.com",
            password="admin",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        self.manager_user = User.objects.create_user(
            username="manager1",
            email="manager1@email.com",
            password="manager1234",
            is_staff=True,
            is_superuser=False,
            is_active=True,
        )

        self.employee_user = User.objects.create_user(
            username="employee1",
            email="employee1@email.com",
            password="employee1234",
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )

        Course.objects.create(
            title="Onboarding 101",
            description="Introduction for new employees",
            status="draft",
        )

    def login_and_get_token(self, email, password):
        response = self.client.post(
            self.LOGIN_URL,
            {
                "email": email,
                "password": password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        return response.data["token"]

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def clear_auth(self):
        self.client.credentials()

    def test_login_admin_success_for_superuser(self):
        response = self.client.post(
            self.LOGIN_URL,
            {
                "email": "admin@email.com",
                "password": "admin",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["id"], self.superuser.id)
        self.assertEqual(response.data["user"]["email"], "admin@email.com")
        self.assertEqual(response.data["user"]["role"], "admin")

    def test_login_admin_success_for_manager(self):
        response = self.client.post(
            self.LOGIN_URL,
            {
                "email": "manager1@email.com",
                "password": "manager1234",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["id"], self.manager_user.id)
        self.assertEqual(response.data["user"]["email"], "manager1@email.com")
        self.assertEqual(response.data["user"]["role"], "admin")

    def test_login_employee_success(self):
        response = self.client.post(
            self.LOGIN_URL,
            {
                "email": "employee1@email.com",
                "password": "employee1234",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["id"], self.employee_user.id)
        self.assertEqual(response.data["user"]["email"], "employee1@email.com")
        self.assertEqual(response.data["user"]["role"], "employee")

    def test_login_invalid_credentials_returns_401(self):
        response = self.client.post(
            self.LOGIN_URL,
            {
                "email": "employee1@email.com",
                "password": "wrongpassword",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid email or password")

    def test_login_missing_fields_returns_422(self):
        response = self.client.post(
            self.LOGIN_URL,
            {
                "email": "",
                "password": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("error", response.data)

    def test_logout_authenticated_user_success(self):
        token = self.login_and_get_token("admin@email.com", "admin")
        self.authenticate(token)

        response = self.client.post(self.LOGOUT_URL, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")

    def test_logout_invalidates_token(self):
        token = self.login_and_get_token("admin@email.com", "admin")
        self.authenticate(token)

        logout_response = self.client.post(self.LOGOUT_URL, format="json")
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        dashboard_response = self.client.get(self.DASHBOARD_URL)
        self.assertEqual(dashboard_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_dashboard_superuser_gets_200(self):
        token = self.login_and_get_token("admin@email.com", "admin")
        self.authenticate(token)

        response = self.client.get(self.DASHBOARD_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_courses", response.data)
        self.assertIn("total_employees", response.data)
        self.assertIn("total_assignments", response.data)

    def test_admin_dashboard_manager_gets_200(self):
        token = self.login_and_get_token("manager1@email.com", "manager1234")
        self.authenticate(token)

        response = self.client.get(self.DASHBOARD_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_dashboard_employee_gets_403(self):
        token = self.login_and_get_token("employee1@email.com", "employee1234")
        self.authenticate(token)

        response = self.client.get(self.DASHBOARD_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_dashboard_unauthenticated_gets_401(self):
        response = self.client.get(self.DASHBOARD_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_courses_admin_gets_200(self):
        token = self.login_and_get_token("manager1@email.com", "manager1234")
        self.authenticate(token)

        response = self.client.get(self.COURSES_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("courses", response.data)
        self.assertGreaterEqual(len(response.data["courses"]), 1)

        first_course = response.data["courses"][0]
        self.assertIn("id", first_course)
        self.assertIn("title", first_course)
        self.assertIn("description", first_course)
        self.assertIn("status", first_course)
        self.assertIn("created_at", first_course)

    def test_get_courses_employee_gets_403(self):
        token = self.login_and_get_token("employee1@email.com", "employee1234")
        self.authenticate(token)

        response = self.client.get(self.COURSES_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_courses_admin_gets_201(self):
        token = self.login_and_get_token("manager1@email.com", "manager1234")
        self.authenticate(token)

        response = self.client.post(
            self.COURSES_URL,
            {
                "title": "Django Basics",
                "description": "Intro for new hires",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("course", response.data)
        self.assertEqual(response.data["course"]["title"], "Django Basics")
        self.assertEqual(response.data["course"]["description"], "Intro for new hires")
        self.assertEqual(response.data["course"]["status"], "draft")
        self.assertIn("created_at", response.data["course"])

    def test_post_courses_missing_title_returns_422(self):
        token = self.login_and_get_token("manager1@email.com", "manager1234")
        self.authenticate(token)

        response = self.client.post(
            self.COURSES_URL,
            {
                "description": "Missing title",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data["error"], "Title is required")

    def test_post_courses_employee_gets_403(self):
        token = self.login_and_get_token("employee1@email.com", "employee1234")
        self.authenticate(token)

        response = self.client.post(
            self.COURSES_URL,
            {
                "title": "Should Fail",
                "description": "Employee cannot create this",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_admin_gets_200_and_only_employee_accounts(self):
        token = self.login_and_get_token("manager1@email.com", "manager1234")
        self.authenticate(token)

        response = self.client.get(self.USERS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("users", response.data)

        returned_emails = [user["email"] for user in response.data["users"]]
        returned_roles = [user["role"] for user in response.data["users"]]

        self.assertIn("employee1@email.com", returned_emails)
        self.assertNotIn("admin@email.com", returned_emails)
        self.assertNotIn("manager1@email.com", returned_emails)

        for role in returned_roles:
            self.assertEqual(role, "employee")

        for user in response.data["users"]:
            self.assertIn("id", user)
            self.assertIn("email", user)
            self.assertIn("role", user)
            self.assertIn("created_at", user)

    def test_get_users_employee_gets_403(self):
        token = self.login_and_get_token("employee1@email.com", "employee1234")
        self.authenticate(token)

        response = self.client.get(self.USERS_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_unauthenticated_gets_401(self):
        response = self.client.get(self.USERS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)