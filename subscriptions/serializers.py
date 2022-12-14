from rest_framework import serializers
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
    product_stripe_id = serializers.CharField(write_only=True)
    success_redirect_url = serializers.CharField(write_only=True)
    cancel_redirect_url = serializers.CharField(write_only=True)

    class Meta:
        fields = ["product_stripe_id", "success_redirect_url", "cancel_redirect_url"]