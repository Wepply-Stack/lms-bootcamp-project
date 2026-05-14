from rest_framework import serializers
from apps.courses_app.models import Lesson, LessonProgress

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "objective",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "course", "order", "created_at", "updated_at"]

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()
    
class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source="lesson.id", read_only=True)

    class Meta:
        model = LessonProgress
        fields = [
            "id",
            "lesson_id",
            "status",
            "started_at",
            "completed_at",
            "updated_at",
        ]
        read_only_fields = fields
