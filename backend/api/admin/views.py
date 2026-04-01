from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsAdmin
from admin.serializers import AdminDashboardSerializer, UserListSerializer
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminDashboardView(APIView):
    """
    Admin dashboard endpoint returning summary statistics.
    Only accessible by admin users.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        # Calculate dashboard metrics
        total_courses = Course.objects.count()
        total_employees = User.objects.filter(role='employee').count()
        total_assignments = 0  # Placeholder for now
        
        data = {
            'total_courses': total_courses,
            'total_employees': total_employees,
            'total_assignments': total_assignments
        }
        
        serializer = AdminDashboardSerializer(data)
        return Response(serializer.data)


class AdminUserListView(APIView):
    """
    List all users with employee role.
    Only accessible by admin users.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        employees = User.objects.filter(role='employee')
        serializer = UserListSerializer(employees, many=True)
        return Response(serializer.data)