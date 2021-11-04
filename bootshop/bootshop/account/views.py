from django.shortcuts import render, reverse, redirect
from order.models import Order
from catalog.models import Product,Category
from catalog.forms import ProductAdminForm, CategoryPostForm
from django.contrib.auth import views
from django.contrib import messages
# Create your views here.


class ManagerLoginView(views.LoginView):
    template_name = 'registration/login.html'


class ManagerLogoutView(views.LogoutView):
    template_name = 'registration/login.html'


def show_manager(request):
    page_title = 'Manager account'
    name = request.user.username
    return render(request, 'manager/index.html', locals())


def show_order(request):
    page_title = "Orders"
    orders = Order.objects.all()
    return render(request, 'manager/order/inventory.html', locals())


def show_product(request):
    page_title = 'products'
    products = Product.active.all()
    return render(request, 'manager/product/inventory.html', locals())


def add_product(request):
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "a new product has been added successfully")
            url = reverse('product_view')
            return redirect(url)
        else:
            messages.error(request, 'there is a error. please correct')
            return render(request, 'manager/product/add.html', {'form': form})

    form = ProductAdminForm()
    page_title = 'new product'
    return render(request, 'manager/product/add.html', {'form': form, 'page_title': page_title})


def show_category(request):
    page_title = "category"
    categories = Category.active.all()
    return render(request, 'manager/categories/inventory.html', locals())


def add_category(request):
    if request.method == 'POST':
        form = CategoryPostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'new category successfully added')
            url = reverse('category_view')
            return redirect(url)
        else:
            messages.error(request, form.errors)
            return render(request, 'manager/categories/add.html', {'form': form})
    page_title = 'add new category'
    form = CategoryPostForm()
    return render(request, 'manager/categories/add.html', {'page_title': page_title, 'form': form})
