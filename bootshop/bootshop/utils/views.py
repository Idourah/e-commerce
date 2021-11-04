from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Product
from order.forms import CheckoutForm
from order.models import Order, OrderItem
from cart import cart
from django.contrib import messages

# Create your views here.


def HomeView(request):
    products = Product.active.all()
    return render(request, 'index.html', {'products': products})

