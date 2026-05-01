import os
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.admin_app.permissions import IsAdmin
from .models import Course, CourseMaterial
from .serializers import CourseSerializer, CourseMaterialSerializer, FileUploadSerializer, FILE_TYPE

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
    

class CourseMaterialViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, JSONParser]

    def get_permissions(self):
        if self.action == "create" or self.action == "destroy":
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]
    
    def list(self, request, course_id=None):
        course = get_object_or_404(Course, id=course_id)
        materials = course.materials.all()
        serializer = CourseMaterialSerializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def create(self, request, course_id=None):
        course = get_object_or_404(Course, id=course_id)
        serializer = FileUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        file = serializer.validated_data["file"]
        extension = os.path.splitext(file.name)[1].lower()
        file_type = FILE_TYPE[extension]
        filename = file.name

        duplicate_exits = CourseMaterial.objects.filter(
            course=course,
            filename=filename
        ).exists()


        if not duplicate_exits:
            material = CourseMaterial.objects.create(
            course = course,
            file = file,
            file_type = file_type,
            filename = file.name,
        )
        else: 
            return Response({"message": "Duplicate file. A file with this same name already exists for this course."},
                            status=status.HTTP_409_CONFLICT)

        return Response(
            CourseMaterialSerializer(material).data, 
            status=status.HTTP_201_CREATED)
    
    def destroy(self, request, course_id=None, pk=None):
        course = get_object_or_404(Course, id=course_id)
        material = get_object_or_404(CourseMaterial, id=pk, course=course)

        if material.file:
            material.file.delete(save=False)
        
        material.delete()

        return Response({"message": "File deleted successfully."},
                        status=status.HTTP_200_OK)