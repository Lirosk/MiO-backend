from django.urls import path

from . import views

urlpatterns = [
     path('payment-session/', views.PaymentSessionAPIView.as_view(), name='payment-session'),
     path('products/', views.ProductsAPIView.as_view(), name='products')
]
