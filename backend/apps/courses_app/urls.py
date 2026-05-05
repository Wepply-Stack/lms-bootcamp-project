from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, MaterialViewSet
from .views import CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

lesson_list = LessonViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

lesson_detail = LessonViewSet.as_view(
    {
        "patch": "partial_update",
        "delete": "destroy",
    }
)

lesson_reorder = LessonViewSet.as_view(
    {
        "patch": "reorder"
    }
)

course_materials = MaterialViewSet.as_view({
    "get": "list",
    "post": "create",
})

course_materials_delete = MaterialViewSet.as_view({
    "delete": "destroy",
})


urlpatterns = [
    path("", include(router.urls)),

    path("courses/<int:course_id>/lessons/",
         lesson_list,
         name="course-lessons",),
    
    path("courses/<int:course_id>/lessons/reorder/",
        lesson_reorder,
        name="course-lessons-reorder",),

    path("courses/<int:course_id>/lessons/<int:pk>/",
         lesson_detail,
         name="course-lesson-detail",),
    
    path("courses/<int:course_id>/<int:lesson_id>/materials/", 
         course_materials, 
         name="course-materials"),
    
    path("courses/<int:course_id>/<int:lesson_id>/materials/<int:pk>/",
         course_materials_delete, 
         name="course-materials-delete"),     
]