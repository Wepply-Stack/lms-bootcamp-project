from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from authentication.permissions import IsAdmin
from courses.models import Course
from courses.serializers import CourseSerializer, CourseCreateSerializer


class CourseListView(APIView):
    """
    List all courses (including drafts).
    Only accessible by admin users.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """
        Get all courses with no filtering.
        """
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseCreateView(APIView):
    """
    Create a new course.
    Only accessible by admin users.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        """
        Create a new course with validation.
        """
        serializer = CourseCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save with created_by from authenticated user
            course = serializer.save(created_by=request.user)
            return Response(
                CourseSerializer(course).data,
                status=status.HTTP_201_CREATED
            )
        
        # Return validation errors
        return Response(
            serializer.errors,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )