from django.db import models
from account.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    view = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductCountView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vproduct')
    user = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user} view {self.product}'
