from cart import cart
from django.urls import reverse
from order.forms import CheckoutForm
from order.models import Order, OrderItem


def get_checkout_url(request):
    return reverse('checkout')


def create_order(request):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.status = Order.SUBMITTED
    order.save()
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price
            oi.product = ci.product
            oi.save()
        cart.empty_cart(request)
    return order
