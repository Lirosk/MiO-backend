from subscriptions.models import Subscriptions, default_product

def set_default_subscription(user):
    subscription = Subscriptions.objects.filter(user=user)

    if not subscription.exists():
        Subscriptions(user=user, product=default_product).save()
        return
    
    subscription = subscription.first()
    subscription.product = default_product
    subscription.subscription = None
    subscription.save()