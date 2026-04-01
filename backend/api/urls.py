from django.urls import path, include

urlpatterns = [
    # Authentication endpoints (shared)
    path('api/auth/', include('auth.urls')),
    
    # Admin endpoints
    path('api/admin/', include('admin.urls')),
    
    # Course endpoints (admin-only)
    path('api/', include('courses.urls')),
]