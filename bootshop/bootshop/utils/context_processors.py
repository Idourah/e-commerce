from catalog.models import Category
from cart import cart
from bootshop import settings
from catalog.models import Product


def shop(request):
    return{
        'site_name': settings.SITE_NAME,
        'cart_items': cart.get_cart_items(request),
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }