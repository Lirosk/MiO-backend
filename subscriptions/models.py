from typing import Tuple, Dict, Any
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from utils.models import TrackingModel
import stripe
stripe.api_key = settings.STRIPE_SECRET_API_KEY

User = get_user_model()


# Create your models here.

class Product(TrackingModel):
    stripe_id = models.CharField(
        unique=True,
        max_length=19,
        null=False,
    )

    name = models.CharField(
        max_length=36,
        null=False
    )

    description = models.CharField(
        max_length=128,
        default=""
    )

    def copy_fields(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("Can't copy fields from another type object.")

        self.name = obj.name
        self.description = obj.description

    @classmethod
    def get_via_API(cls):
        products_data = stripe.Product.list(active=True).data
        products = []
        for product_data in products_data:
            if not product_data["name"].startswith("MiO"):
                continue

            product = cls(
                name=product_data["name"],
                description=product_data["description"],
                stripe_id=product_data["id"]
            )
            products.append(product)

        for product in products:
            try:
                saved_product = cls.objects.get(stripe_id=product.stripe_id)
                saved_product.copy_fields(product)
                saved_product.save()    
            except cls.DoesNotExist:
                product.save()

        for product_data in products_data:
            try:
                price = Price.objects.get(stripe_id=product_data["default_price"])
                product = Product.objects.get(stripe_id=product_data["id"])

                if not ProductPriceFeature.objects.filter(price=price, product=product):
                    ProductPriceFeature(price=price, product=product).save()
            except (Price.DoesNotExist, Product.DoesNotExist):
                ...


class Price(models.Model):
    stripe_id = models.CharField(
        unique=True,
        max_length=30,
        null=False,
    )

    per_unit = models.IntegerField(
        null=False
    )

    period = models.CharField(
        max_length=16,
        null=False
    )

    currency = models.CharField(
        max_length=16,
        null=False
    )

    def copy_fields(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("Can't copy fields from another type object.")

        self.per_unit = obj.per_unit
        self.period = obj.period
        self.currency = obj.currency

    @classmethod
    def get_via_API(cls):
        prices_data = stripe.Price.list().data

        prices_and_products = []
        for price_data in prices_data:
            try:
                price_and_product = cls(
                    stripe_id = price_data["id"],
                    per_unit = price_data["unit_amount"],
                    period = price_data["recurring"]["interval"],
                    currency = price_data["currency"]
                )

                prices_and_products.append({"price": price_and_product, "product": price_data["product"]})
            except Product.DoesNotExist:
                ...
                
        for price_and_product in prices_and_products:
            price = price_and_product["price"]
            product_id = price_and_product["product"]

            try:
                saved_price = cls.objects.get(stripe_id=price.stripe_id)
                saved_price.copy_fields(price)
                saved_price.save()
            except cls.DoesNotExist:
                price.save()

            prods = [*Product.objects.all()]
            product = Product.objects.filter(stripe_id=product_id)

            if not product.exists():
                continue
            product = product.first()

            stored_price_and_product = ProductPriceFeature.objects.filter(product=product, price=price)
            if not stored_price_and_product.exists():
                ProductPriceFeature(product=product, price=price)


class Feature(models.Model):
    description = models.CharField(
        blank=True,
        max_length=126
    )


class ProductPriceFeature(models.Model):
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE)
    price = models.OneToOneField(to=Price, on_delete=models.CASCADE)
    features = models.ManyToManyField(to=Feature)


class Subscriptions(TrackingModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    subscription = models.CharField(
        max_length=36,
        null=True
    )

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
        if self.subscription:
            stripe.Subscription.delete(self.subscription)
        self.product = default_product
        self.subscription = None
        self.save()


default_product = Product.objects.get(stripe_id="prod_MxPEoLynfedPOv")