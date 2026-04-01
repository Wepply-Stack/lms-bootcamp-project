from rest_framework import serializers
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()


class AdminDashboardSerializer(serializers.Serializer):
    """Serializer for admin dashboard data"""
    total_courses = serializers.IntegerField()
    total_employees = serializers.IntegerField()
    total_assignments = serializers.IntegerField()


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing employee users"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']