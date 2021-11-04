from django.shortcuts import render, redirect, reverse
from order.models import Order, OrderItem
from order.forms import CheckoutForm
from cart.models import CartItem
from cart import cart
from order import checkout

# Create your views here.


def show_checkout(request):
    if cart.is_empty(request):
        url = reverse('cart')
        return redirect(url)
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = CheckoutForm(post_data)
        if form.is_valid():
            order = checkout.create_order(request)
            order_number = order.id
            if order_number:
                request.session['order_number'] = order_number
                return redirect('receipt')
        else:
            error_message = 'Correct the errors below'
    else:
        form = CheckoutForm()
    page_title = 'Checkout'
    cart_total = cart.sub_total(request)
    return render(request, 'checkout/checkout.html', locals())


def receipt(request):
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
    else:
        return redirect('show_cart')
    return render(request, 'checkout/receipt.html', locals())