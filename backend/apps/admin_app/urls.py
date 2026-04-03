from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminDashboardView, CourseViewSet, UsersView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('/', include(router.urls)),
    path('users/', UsersView.as_view(), name='users'),
]
