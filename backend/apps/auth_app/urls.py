from django.urls import path
from .views import CookieTokenRefreshView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
