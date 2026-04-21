from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.admin_app.permissions import IsAdmin
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = CourseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        course = Course.objects.create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description", ""),
            status="draft",
        )

        return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)