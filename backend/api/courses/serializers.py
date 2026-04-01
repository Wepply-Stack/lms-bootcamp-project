from rest_framework import serializers
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model with validation.
    """
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        """
        Validate that title is not empty and has minimum length.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long"
            )
        
        return value.strip()
    
    def validate_status(self, value):
        """
        Validate status is one of allowed choices.
        """
        allowed_statuses = ['draft', 'published', 'archived']
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(allowed_statuses)}"
            )
        return value


class CourseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new courses with required validation.
    """
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_title(self, value):
        """
        Required field validation for title.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Title is required")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long"
            )
        
        # Check for duplicate titles (optional)
        if Course.objects.filter(title__iexact=value.strip()).exists():
            raise serializers.ValidationError(
                "A course with this title already exists"
            )
        
        return value.strip()
    
    def create(self, validated_data):
        """
        Create course with default status if not provided.
        """
        if 'status' not in validated_data:
            validated_data['status'] = 'draft'
        
        return super().create(validated_data)