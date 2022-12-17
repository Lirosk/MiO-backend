from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from . import models
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


class PaymentSessionAPIView(GenericAPIView):
    serializer_class = serializers.PaymentSessionSerializer
    
    product_stripe_id = openapi.Parameter(
        'product_stripe_id', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    success_redirect_url = openapi.Parameter(
        'success_redirect_url', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    cancel_redirect_url = openapi.Parameter(
        'cancel_redirect_url', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[product_stripe_id, success_redirect_url, cancel_redirect_url])
    def get(self, request):
        serialized = self.serializer_class(data=request.GET)
        serialized.is_valid(raise_exception=True)

        try:
            product = models.Product.objects.get(stripe_id=serialized.data["product_stripe_id"])

            ppf = models.ProductPriceFeature.objects.get(product=product)

            checkout_session = models.stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=["card"],
                line_items=[{
                    "price": ppf.price.stripe_id,
                    "quantity": 1,
                }],
                metadata={
                    "product": serialized.data["product_stripe_id"],
                },
                mode="subscription",
                success_url = serialized.data["success_redirect_url"],
                cancel_url = serialized.data["cancel_redirect_url"],
            )

            return Response({"checkout_url": checkout_session.url}, status=status.HTTP_200_OK)
        except (models.Product.DoesNotExist, models.ProductPriceFeature.DoesNotExist):
            return Response({"message": "Product with such id does not exists."}, status=status.HTTP_400_BAD_REQUEST)


class ProductsAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
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
                product_data["features"].append(serilized_feature.data["description"])

            data.append(product_data)

        return Response(data, status=status.HTTP_200_OK)


class StripeWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        payload = request.body

        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = models.stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return Response({"message": "Invalid payload."}, status=status.HTTP_400_BAD_REQUEST)
        except models.stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response({"message": "Invalid signature."}, status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == 'customer.subscription.deleted':
            ...
        if event['type'] == 'checkout.session.completed':
            # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
            session = models.stripe.checkout.Session.retrieve(
                event['data']['object']['id'],
                expand=['line_items'],
            )

            email = session["customer_email"]
            product = session["metadata"]["product"]

            try:
                user = User.objects.get(email=email)
                product = models.Product.objects.get(stripe_id=product)
                subscription = session["subscription"]

                models.Subscriptions(user=user, product=product, subscription=subscription).save()
                
            except (User.DoesNotExist, models.Product.DoesNotExist):
                return Response({"message": "User with such email or product with such id doesn't exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)


class CancelSubscriptionAPIView(GenericAPIView):
    serializer_class = serializers.CancelSubscriptionSerializer

    def post(self, request):
        serialized = self.serializer_class(data={"email": request.user.email, "password": request.data.get("password")})
        serialized.is_valid(raise_exception=True)

        user = User.objects.get(email=serialized.data["email"])

        try:
            subscription = models.Subscriptions.objects.get(user=user)
            subscription.delete()
        except models.Subscriptions.DoesNotExist:
            ...
        
        return Response({}, status=status.HTTP_200_OK)