from rest_framework import serializers
from apps.auth_app.models import User

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']

class DashboardSerializer(serializers.Serializer):
    total_courses = serializers.IntegerField()
    total_employees = serializers.IntegerField()
    total_assignments = serializers.IntegerField()