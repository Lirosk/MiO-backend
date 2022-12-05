from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    # path('register/', views.RegisterView.as_view()),
    # path('reset/'),
    # path('refresh/'),
]