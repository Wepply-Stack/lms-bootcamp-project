from django.db import models

class Course(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    # created_by = models.ForeignKey(
    #     "auth_app.User",
    #     on_delete=models.CASCADE,
    #     related_name="created_courses",
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "courses"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
class CourseMaterial(models.Model):
    FILE_TYPE_CHOICES = [
        ("pdf", "PDF"),
        ("audio", "AUDIO"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="materials"
    )
    
    file = models. FileField(upload_to="course_material/")
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "course_materials"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.filename