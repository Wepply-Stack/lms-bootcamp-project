from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, CourseMaterialViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

course_materials = CourseMaterialViewSet.as_view({
    "get": "list",
    "post": "create",
})

course_materials_delete = CourseMaterialViewSet.as_view({
    "delete": "destroy",
})

urlpatterns = [
    path("", include(router.urls)),
    path("courses/<int:course_id>/materials/", course_materials, name="course-materials"),
    path("courses/<int:course_id>/materials/<int:pk>/",course_materials_delete, name="course-materials-delete"),
]