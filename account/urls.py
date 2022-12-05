from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('user/', views.AuthUserAPIView.as_view()),
]
