from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('verify-email/', views.EmailVerificationAPIView.as_view(), name='verify-email'),
    path("password-reset/in-place/", views.PasswordResetInPlaceAPIView.as_view(), name="password-reset-in-place"),
    path('password-reset/via-email/', views.PasswordResetAPIView.as_view(), name="password-reset"),
    path('password-reset/set-new/', views.SetNewPasswordAPIView.as_view(), name="set-new-password"),
]