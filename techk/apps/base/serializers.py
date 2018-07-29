from rest_framework import serializers
from .models import Category, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'status',)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title', 
            'category_id', 
            'thumbnail', 
            'price', 
            'stock',
            'stock_count', 
            'upc', 
            'product_description',
            'status',
            )