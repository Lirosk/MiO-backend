from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["stripe_id", "name", "description"]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        fields = ["stripe_id", "per_unit", "period", "currency"]


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feature
        fields = ["description"]


class PaymentSessionSerializer(serializers.Serializer):
    product_stripe_id = serializers.CharField()
    success_redirect_url = serializers.CharField()
    cancel_redirect_url = serializers.CharField()

    class Meta:
        fields = ["product_stripe_id", "success_redirect_url", "cancel_redirect_url"]


class CancelSubscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ["password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials.")

        return super().validate(attrs)