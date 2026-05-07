from rest_framework import serializers
from apps.auth_app.models import User

class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'position', 'role', 'created_at']
        read_only_fields = ['id', 'role', 'created_at']

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'position', 'role', 'created_at']
        read_only_fields = ['id', 'role', 'created_at']

class CreateEmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    position = serializers.CharField(max_length=100, required=False, allow_blank=True)
    password_option = serializers.ChoiceField(choices=['auto', 'lastname'], default='auto')
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

class EmployeeDeleteSerializer(serializers.Serializer):
    # Allows multiple/mass deletion
    employee_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate_employee_ids(self, value):
        unique_ids = list(dict.fromkeys(value))
        if not unique_ids:
            raise serializers.ValidationError("employee_ids must be a non-empty list.")
        return unique_ids

class DashboardSerializer(serializers.Serializer):
    total_courses = serializers.IntegerField()
    total_employees = serializers.IntegerField()
    total_assignments = serializers.IntegerField()

class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    phone_number = serializers.CharField(max_length=20, required=False)
    position = serializers.CharField(max_length=100, required=False)

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

