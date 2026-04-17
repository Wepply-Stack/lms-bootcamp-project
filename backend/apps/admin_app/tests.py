from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.auth_app.models import User
from apps.admin_app import views

class AdminAccessTests(TestCase):
    
    def setUp(self):
        views.courses_db.clear()
        views.course_id_counter = 1
        self.client = APIClient()
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        
        # Create employee user
        self.employee_user = User.objects.create_user(
            email='employee@example.com',
            password='employeepass123',
            role='employee'
        )
        
        # Generate tokens
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.employee_token = str(RefreshToken.for_user(self.employee_user).access_token)
    
    def test_admin_can_access_dashboard(self):
        """Test that admin users can access the dashboard"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/admin/dashboard/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_courses', response.data)
        self.assertIn('total_employees', response.data)
    
    def test_employee_cannot_access_dashboard(self):
        """Test that employee users cannot access admin dashboard"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.employee_token}')
        response = self.client.get('/api/admin/dashboard/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_create_course(self):
        """Test that admin users can create courses"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post('/api/courses/', {
            'title': 'Test Course',
            'description': 'This is a test course'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Course')
        self.assertEqual(response.data['status'], 'draft')
    
    def test_admin_cannot_create_course_without_title(self):
        """Test that course creation fails without title"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post('/api/courses/', {
            'description': 'No title provided'
        })
        
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def test_employee_cannot_create_course(self):
        """Test that employee users cannot create courses"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.employee_token}')
        response = self.client.post('/api/courses/', {
            'title': 'Test Course'
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_list_employees(self):
        """Test that admin users can list all employees"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
    
    def test_employee_cannot_list_employees(self):
        """Test that employee users cannot list employees"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.employee_token}')
        response = self.client.get('/api/users/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot access admin routes"""
        response = self.client.get('/api/admin/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.post('/api/courses/', {'title': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_can_list_courses(self):
        """Test that admin users can list all courses"""
        # First create a course
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.client.post('/api/courses/', {'title': 'Course 1'})
        
        # Then list courses
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
