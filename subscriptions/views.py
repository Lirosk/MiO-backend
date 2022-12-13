from django.http import HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import models
from . import serializers
# Create your views here.


class PaymentSessionAPIView(GenericAPIView):
    authentication_classes = []

    def get(self, request):
        prices = models.stripe.Price.list()

        checkout_session = models.stripe.checkout.Session.create(
            line_items=[{
                'price': prices.data[1].id,
                'quantity': 1
            }],
            mode='subscription',
            success_url='http://google.com',
            cancel_url='http://yandex.com'
        )

        return HttpResponseRedirect(checkout_session.url)


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