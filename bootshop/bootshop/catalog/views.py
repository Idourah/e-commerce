from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Category, Product
from django.core.paginator import Paginator
from cart.forms import ProductAddToCartForm
from cart import cart
# Create your views here.


def index(request):
    page_title = 'natural ointment, peeling, dermal filter'
    p = Paginator(Product.active.all(), 6)
    page = request.GET.get('page')
    products = p.get_page(page)
    nums = 'a' * products.paginator.num_pages
    return render(request, 'catalog/product_list.html', locals())


def show_category(request, slug):
    c = get_object_or_404(Category, slug=slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, 'catalog/product_list.html', locals())


def show_product(request, slug):
    p = get_object_or_404(Product, slug=slug)
    categories = p.categories.all()
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # Check for Post request if submitted bu user
    if request.method == 'POST':
        # copy data send by user, quantity and product slug
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        if form.is_valid():
            # add product to cart
            cart.add_to_cart(request)
            # get rid of cookies if found
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = reverse('cart')
            return redirect(url)
    else:
        # if user send a GET request, create a simple form
        form = ProductAddToCartForm(request=request, label_suffix='')
    # bound hidden field value with product slug
    form.fields['product_slug'].widget.attrs['value'] = slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    return render(request, 'catalog/product_detail.html', locals())


def show_bestseller(request):
    products = Product.active.filter(is_bestseller=True)
    return render(request, 'catalog/best_seller.html', {'products': products})


def show_featured(request):
    products = Product.active.filter(is_featured=True)
    return render(request, 'catalog/top_featured.html', {'products': products})


def results(request):
    search_text = request.GET.get('q', '')
    result = Product.active.filter(name__icontains=search_text)
    return render(request, 'catalog/search.html', {'result': result})


