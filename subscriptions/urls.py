from django.urls import path
from . import views

urlpatterns = [
     path('create/', views.CreatePaymentSessionAPIView.as_view()),
]
