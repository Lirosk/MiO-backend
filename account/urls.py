from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    # path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    # path('register/', views.RegisterView.as_view()),
    # path('reset/'),
    # path('refresh/'),
]