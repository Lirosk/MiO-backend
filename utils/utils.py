from subscriptions.models import Subscriptions, default_product
from main import APIs
from subscriptions.models import default_product

def set_default_subscription(user):
    subscription = Subscriptions.objects.filter(user=user)

    if not subscription.exists():
        Subscriptions(user=user, product=default_product).save()
        return
    
    subscription = subscription.first()
    subscription.product = default_product
    subscription.subscription = None
    subscription.save()


def can_user_connect_more_social_networks(user):
    ppf = Subscriptions.objects.get(user=user)
    if ppf.product.stripe_id != default_product.stripe_id:
        return True

    limit = 1
    have = 0
    for api in APIs.available.values():
        if api.is_user_authorized(user):
            have += 1

    result = limit > have
    return result