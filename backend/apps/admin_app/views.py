from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from .serializers import (
    CourseSerializer, EmployeeProfileSerializer, DashboardSerializer, 
    CreateEmployeeSerializer, UpdateProfileSerializer, ChangePasswordSerializer
)
from apps.auth_app.models import User
import secrets
import string

courses_db = []
course_id_counter = 1

def generate_random_password(length=8):
    """Generate random password with letters, numbers, and special characters"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        data = {
            'total_courses': len(courses_db),
            'total_employees': User.objects.filter(role='employee').count(),
            'total_assignments': 0
        }
        serializer = DashboardSerializer(data)
        return Response(serializer.data)

class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def list(self, request):
        return Response(courses_db)
    
    def create(self, request):
        global course_id_counter
        
        serializer = CourseSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        if 'title' not in request.data or not request.data['title']:
            return Response(
                {'title': ['This field is required']},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        course = {
            'id': course_id_counter,
            'title': serializer.validated_data['title'],
            'description': serializer.validated_data.get('description', ''),
            'status': 'draft',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z'
        }
        
        courses_db.append(course)
        course_id_counter += 1
        
        return Response(course, status=status.HTTP_201_CREATED)

class UsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        employees = User.objects.filter(role='employee')
        serializer = EmployeeProfileSerializer(employees, many=True)
        return Response(serializer.data)

class CreateEmployeeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        serializer = CreateEmployeeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        validated_data = serializer.validated_data
        
        # Generate password based on option
        if validated_data['password_option'] == 'lastname':
            generated_password = validated_data['last_name'].upper()
        else:  # auto
            generated_password = generate_random_password()
        
        # Create employee user with full profile
        user = User.objects.create_user(
            email=validated_data['email'],
            password=generated_password,
            role='employee',
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
            position=validated_data.get('position', '')
        )
        
        return Response({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'position': user.position,
            'role': user.role,
            'generated_password': generated_password,
            'message': f'Employee created successfully. Password is: {generated_password}'
        }, status=status.HTTP_201_CREATED)

class EmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current employee's profile"""
        if request.user.role != 'employee':
            return Response(
                {'error': 'Only employees can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = EmployeeProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update employee's own profile"""
        if request.user.role != 'employee':
            return Response(
                {'error': 'Only employees can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UpdateProfileSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        user = request.user
        for field, value in serializer.validated_data.items():
            if value:
                setattr(user, field, value)
        user.save()
        
        return Response({
            'message': 'Profile updated successfully',
            'profile': EmployeeProfileSerializer(user).data
        })
    
    def patch(self, request):
        """Partial update employee's profile"""
        return self.put(request)

class EmployeeChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Employee changes their own password"""
        if request.user.role != 'employee':
            return Response(
                {'error': 'Only employees can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ChangePasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Check current password
        if not request.user.check_password(serializer.validated_data['current_password']):
            return Response(
                {'current_password': ['Wrong password']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': 'Password changed successfully'})

