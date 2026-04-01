import jwt
import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings

from courses.models import Course

User = get_user_model()


class AdminAccessTests(TestCase):
    """
    Test cases for admin-only endpoints.
    """
    
    def setUp(self):
        self.client = APIClient()
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        
        # Create employee user
        self.employee_user = User.objects.create_user(
            email='employee@example.com',
            password='employee123',
            role='employee'
        )
        
        # Create some test courses
        self.course1 = Course.objects.create(
            title='Test Course 1',
            description='Test Description',
            status='draft',
            created_by=self.admin_user
        )
        
        self.course2 = Course.objects.create(
            title='Test Course 2',
            description='Another course',
            status='published',
            created_by=self.admin_user
        )
    
    def generate_token(self, user):
        """Helper method to generate JWT token for a user"""
        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    def test_admin_dashboard_access_success(self):
        """Test admin can access dashboard"""
        token = self.generate_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/admin/dashboard/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_courses', response.data)
        self.assertIn('total_employees', response.data)
        self.assertEqual(response.data['total_courses'], 2)
        self.assertEqual(response.data['total_employees'], 1)
    
    def test_employee_dashboard_access_denied(self):
        """Test employee cannot access admin dashboard"""
        token = self.generate_token(self.employee_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/admin/dashboard/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_course_list_access(self):
        """Test admin can list all courses"""
        token = self.generate_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/courses/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_employee_course_list_access_denied(self):
        """Test employee cannot list courses"""
        token = self.generate_token(self.employee_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/courses/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_create_course_success(self):
        """Test admin can create a course"""
        token = self.generate_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        data = {
            'title': 'New Course',
            'description': 'Course description',
        }
        
        response = self.client.post('/api/courses/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Course')
        self.assertEqual(response.data['status'], 'draft')
        self.assertEqual(Course.objects.count(), 3)
    
    def test_admin_create_course_missing_title(self):
        """Test admin cannot create course without title"""
        token = self.generate_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        data = {
            'description': 'No title provided',
        }
        
        response = self.client.post('/api/courses/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('title', response.data)
    
    def test_admin_list_employees(self):
        """Test admin can list all employees"""
        token = self.generate_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Create additional employees
        User.objects.create_user(
            email='employee2@example.com',
            password='password123',
            role='employee'
        )
        
        response = self.client.get('/api/admin/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two employees total
        for user in response.data:
            self.assertEqual(user['role'], 'employee')
    
    def test_unauthenticated_access(self):
        """Test unauthenticated requests are rejected"""
        response = self.client.get('/api/admin/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_invalid_token(self):
        """Test invalid token is rejected"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.token.here')
        
        response = self.client.get('/api/admin/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)