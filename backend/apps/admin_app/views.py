from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from .serializers import CourseSerializer, EmployeeSerializer, DashboardSerializer
from apps.auth_app.models import User

courses_db = []
course_id_counter = 1

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """
        GET /api/admin/dashboard
        Returns dashboard statistics
        """
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
        """
        GET /api/courses
        Returns all courses (including drafts)
        """
        return Response(courses_db)
    
    def create(self, request):
        """
        POST /api/courses
        Creates a new course
        """
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
        """
        GET /api/users
        Returns all users with role = "employee"
        """
        employees = User.objects.filter(role='employee')
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)