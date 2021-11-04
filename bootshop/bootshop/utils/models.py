from django.db import models

# Create your models here.


class Carousel(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='carousel')
    text = models.TextField()

    class Meta:
        db_table = 'carousels'
        verbose_name_plural = 'carousels'

