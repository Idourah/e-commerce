from django.contrib import admin
from django.urls import path, include
from catalog import views as catalog_view
from search.views import results

urlpatterns = [
    path('inventory/', catalog_view.index, name='product'),
    path('<slug:slug>/products/', catalog_view.show_category, name='category'),
    path('<slug:slug>/detail/', catalog_view.show_product, name='product_detail'),
    path('bestseller/', catalog_view.show_bestseller, name='best_seller'),
    path('featured/', catalog_view.show_featured, name='featured'),
    path('search/results/', results, name='search_results'),

]
