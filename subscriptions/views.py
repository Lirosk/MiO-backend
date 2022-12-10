import stripe
from django.conf import settings
from django.http import HttpResponseRedirect 
from rest_framework.generics import GenericAPIView

stripe.api_key = settings.STRIPE_SECRET_API_KEY
# Create your views here.

class CreatePaymentSessionAPIView(GenericAPIView):
    authentication_classes = []

    def get(self, request):
        prices = stripe.Price.list()

        checkout_session = stripe.checkout.Session.create(
            line_items = [{
                'price': prices.data[1].id,
                'quantity': 1
            }],
            mode='subscription',
            success_url='http://google.com',
            cancel_url='http://yandex.com'
        )

        return HttpResponseRedirect(checkout_session.url)