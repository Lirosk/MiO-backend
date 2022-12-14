from django.http import HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from . import models
from . import serializers
# Create your views here.


class PaymentSessionAPIView(GenericAPIView):
    serializer_class = serializers.PaymentSessionSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    

    def get(self, request):
        serialized = self.serializer_class(request.GET)

        try:
            product = models.Product.objects.get(stripe_id=serialized["product_stripe_id"])

            ppf = models.ProductPriceFeature(product=product)

            checkout_session = models.stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": ppf.price.currency,
                        "unit_amount": ppf.price.per_unit,
                        "product_data": {
                            "name": ppf.product.name,
                        }
                    },
                    "quantity": 1,
                }],
                mode="subscription",
                success_url = serialized.data["success_redirect_url"],
                cancel_url = serialized.data["cancel_redirect_url"],
            )

            return HttpResponseRedirect(checkout_session.url)
        except (models.Product.DoesNotExist, models.ProductPriceFeature.DoesNotExist):
            return Response({"message": "Product with such id does not exists."}, status=status.HTTP_400_BAD_REQUEST)


class ProductsAPIView(APIView):
    def get(self, request):
        if models.Product.objects.count() == 0:
            models.Product.get_via_API()

        if models.Price.objects.count() == 0:
            models.Price.get_via_API()

        products_and_prices = models.ProductPriceFeature.objects.all().select_related()
        data = []
        for product_and_price in products_and_prices:
            serialized_product = serializers.ProductSerializer(product_and_price.product)
            serialized_price = serializers.PriceSerializer(product_and_price.price)
            
            product_data = serialized_product.data
            product_data["price"] = serialized_price.data
            product_data["features"] = []

            features = product_and_price.features.select_related()
            for feature in features:
                serilized_feature = serializers.FeatureSerializer(feature)
                product_data["features"].append(serilized_feature.data)

            data.append(product_data)

        return Response({"products": data}, status=status.HTTP_200_OK)