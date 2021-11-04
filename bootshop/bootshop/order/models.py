import decimal
import time

from django.db import models
from django import forms
import uuid
from catalog.models import Product
from django.utils import timezone
# Create your models here.

BANK_TRANSFERT = 1
WESTERN_UNION = 2
MONEY_GRAM = 3
RIA = 4
PAYSEND = 5
BITCOIN = 6

class Order(models.Model):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    # set of possible order
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (PROCESSED, 'Processed'),
                      (SHIPPED, 'Shipped'),
                      (CANCELLED, 'Cancelled'),)

    # order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    shipping_name = models.CharField(max_length=50)

    # contact info
    email = models.EmailField()
    phone = models.CharField(max_length=20, default='555-555-5555')

    # shipping information

    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=10)


    CHOICES = ((BANK_TRANSFERT, 'BANK TRANSFERT'),
               (WESTERN_UNION,'WESTERN UNION'),
               (MONEY_GRAM,'MONEY GRAM'),
               (RIA, 'RIA'),
               (PAYSEND, 'PAYSEND'),
               (BITCOIN, 'BIT COIN'), )

    payment = models.IntegerField(verbose_name='payment mode', choices=CHOICES, default=BANK_TRANSFERT)

    def __unicode__(self):
        return 'Order #' + str(self.id)

    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    @property
    def total(self):
        return self.quantity + self.price

    @property
    def name(self):
        return self.product.name

    def __unicode__(self):
        return self.product.name

    def get_absolute_url(self):
        return self.product.get_absolute_url()
