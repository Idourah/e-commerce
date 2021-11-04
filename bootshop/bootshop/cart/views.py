from django.shortcuts import render, redirect, reverse
from cart import cart

# Create your views here.


def show_cart(request):
    url = ''
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
            url = reverse('cart')
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
    cart_item_count = cart.cart_item_count(request)
    cart_items = cart.get_cart_items(request)
    cart_total = cart.sub_total(request)
    page_title = 'shopping cart'
    return render(request, 'cart/cart.html', locals())


def checkout(request):
    return render(request, 'checkout.html', {})


