from django.shortcuts import render
from search import search
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bootshop import settings
from django.http import JsonResponse
from catalog.models import  Product
from django.db.models import Q

# Create your views here.


def results(request):
    context = {}
    q = request.GET.get('q', '')
    # get current page number.
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1
    # retrieve the matching products
    matching = search.search_products(q).get('products')
    # generate the paginator object
    paginator = Paginator(matching, settings.PRODUCTS_PER_PAGE)
    try:
        result = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        result = paginator.page(1).object_list

    # store the search
    search.store(request, q)
    page_title = 'search Result for:' + q
    context["page_title"] = page_title
    context["paginator"] = paginator
    context["result"] = result
    if request.is_ajax():
        json_data = list(result.values())
        return JsonResponse({'data':json_data}, status=200)
    return render(request, 'catalog/search.html', context)


def search_json(request):
    term = request.GET.get("q")
    products = search.search_products(term).get("products")
    if request.is_ajax():
        json_data = list(products.values())
        return JsonResponse({'products': json_data}, status=200)
    return render(request, 'catalog/search.html', locals())

