from django.urls import path, include
from django.contrib.auth import views
from account import views as account_view
from bootshop import settings

urlpatterns = [
    path('login/', account_view.ManagerLoginView.as_view(), name='login'),
    path('logout/', account_view.ManagerLogoutView.as_view(), name='logout'),
    path('manager_account/', account_view.show_manager, name='show_manager'),
    path('orders/', account_view.show_order, name='order_view'),
    path('products/', account_view.show_product, name='product_view'),
    path('product/add/', account_view.add_product, name='add_product'),
    path('category/', account_view.show_category, name='category_view'),
    path('category/add/', account_view.add_category, name='add_category'),
]