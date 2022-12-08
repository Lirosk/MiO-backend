from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('user/', views.AuthUserAPIView.as_view(), name='user'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email')
]