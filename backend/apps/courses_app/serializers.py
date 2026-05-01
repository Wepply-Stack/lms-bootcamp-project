import os
from rest_framework import serializers
from .models import Course, CourseMaterial

FILE_TYPE = {
    ".pdf" : "pdf",
    ".mp3" : "audio",
    ".wav" : "audio",
    ".m4a" : "audio",
    ".aac" : "audio",
    ".ogg" : "audio",
}

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "status", "created_at", "updated_at"]
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ["id","course","file","file_type","filename","uploaded_at"]    
        read_only_fields = ["id", "course", "file_type", "filename", "uploaded_at"]
        
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        max_size = 10 * 1024 * 1024 # 10MB
        extension = os.path.splitext(file.name)[1].lower()
        
        if file.size > max_size:
            raise serializers.ValidationError("File size must not exceed 10MB!")
        
        if extension not in FILE_TYPE:
            raise serializers.ValidationError("Unsupported file type. Only PDF and certain audio files are allowed")

        return file
