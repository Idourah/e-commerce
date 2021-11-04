from django.db import models
from catalog.models import Product

# Create your models here.


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def total(self):
        return self.product.price * self.quantity

    def name(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()

    def get_absolute_url(self):
        return self.product.get_absolute_url()
