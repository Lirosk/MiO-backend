from django.urls import path
from . import views

from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.
urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.register_view),
    # path('register/', views.RegisterView.as_view()),
    # path('reset/'),
    # path('refresh/'),
]