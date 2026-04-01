from django.urls import path
from courses.views import CourseListView, CourseCreateView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
]