from django import template
from cart import cart
from catalog.models import Category
from django.core.paginator import Paginator
import urllib

register = template.Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart.cart_item_count(request)
    return {'cart_item_count': cart_item_count}


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = Category.active.all()
    return {
        'active_categories': active_categories,
        'request_path': request_path
    }



