from django import forms

# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Category, Book

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'thumbnail', 'stock', 'product_description',
                'upc', 'category']