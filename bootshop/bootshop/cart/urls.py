from django.urls import path
from .views import show_cart


urlpatterns = [
        path('cart/', show_cart, name='cart'),

]