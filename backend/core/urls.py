from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/login', views.login_view, name='login'),
    path('api/auth/logout', views.logout_view, name='logout'),
    path('api/admin/dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('api/users', views.user_list, name='user-list'),
    path('api/courses', views.courses_view, name='courses'),


    #path('signup', views.signup),
    #path('test_token', views.test_token),
]
