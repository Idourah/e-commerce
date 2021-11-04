from django.shortcuts import render
from search import search
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bootshop import  settings

# Create your views here.


def results(request):
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
    return render(request, 'catalog/search.html', locals())

