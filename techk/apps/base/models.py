from django.db import models

# Create your models here.

# Clase correspondiente a la tabla categoria
class Category(models.Model):
    name = models.CharField(max_length=25)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# clase correspondiente a la tabla libros
class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=10)
    stock = models.BooleanField()
    stock_count = models.IntegerField(blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    upc = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title