########################################################
#                                                      #
#                                                      #
########################################################
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.


class ActiveCategoryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)


class Category(models.Model):
    """
    Category model class to simulate a real product category like
    in real shop
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text="Unique value for product page URL, created from name")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta keywords", max_length=255,
                                     help_text="comma-delimited set of SEO keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    active = ActiveCategoryManager()

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class ActiveProductManager(models.Manager):
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text="Unique value for product URL, created from name")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, blank=True)
    image = models.ImageField(upload_to='images/products')
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField(max_length=255,
                                     help_text="Comma-delimited set of SEO for keyword meta tag")
    meta_description = models.CharField(max_length=255,
                                        help_text="content for Description meta tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    objects = models.Manager
    active = ActiveProductManager()

    class Meta:
        db_table = 'Products'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)



