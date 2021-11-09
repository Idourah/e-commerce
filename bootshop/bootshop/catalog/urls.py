from django.contrib import admin
from django.urls import path, include
from catalog import views as catalog_view
from search import views as search_view

urlpatterns = [
    path('inventory/', catalog_view.index, name='product'),
    path('<slug:slug>/products/', catalog_view.show_category, name='category'),
    path('<slug:slug>/detail/', catalog_view.show_product, name='product_detail'),
    path('bestseller/', catalog_view.show_bestseller, name='best_seller'),
    path('featured/', catalog_view.show_featured, name='featured'),
    path('search/', search_view.search_json, name='search_results'),

]
