from django.db import models


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('product:product_list_search',
                       args=[self.category_name])
