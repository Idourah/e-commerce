import random
import decimal
from .models import CartItem
from django.shortcuts import get_object_or_404
from catalog.models import Product
from order.forms import CheckoutForm

CART_ID_SESSION_KEY = 'cart_id'


# get the current user's cart id, sets new one if blank
def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    cart_id = ''
    characters = 'ABCEDFGHIJKLMNOPKRSTUVWYZabcdefghijklmnopqrstuvwyz' \
                 '1234567890!@#$%^&*()'
    card_id_length = 50
    for y in range(card_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id


# return all items from the current user's cart
def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))


# add an item to the cart
def add_to_cart(request):
    postdata = request.POST.copy()
    # get product slug from post data, return blank if empty
    product_slug = postdata.get('product_slug')
    # get quantity added, return blank if empty
    quantity = postdata.get('quantity', 1)
    # fetch the product or return a missing page error
    p = get_object_or_404(Product, slug=product_slug)
    # get product in cart
    cart_products = get_cart_items(request)
    product_in_cart = False
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            # update the quantity if found
            cart_item.augment_quantity(quantity)
            product_in_cart = True
    if not product_in_cart:
        # create and save a new cart item
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()


def cart_item_count(request):
    return get_cart_items(request).count()


def get_single_cart(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


def update_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    item = get_single_cart(request, item_id)
    if item:
        if int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
        else:
            remove_from_cart(request)


def remove_from_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    item = get_single_cart(request, item_id)
    if item:
        item.delete()


def sub_total(request):
    cart_total = decimal.Decimal('0.00')
    items = get_cart_items(request)
    for item in items:
        cart_total += item.product.price * item.quantity
    return cart_total


def is_empty(request):
    return cart_item_count(request) == 0


def empty_cart(request):
    user_cart = get_cart_items(request)
    user_cart.delete()

