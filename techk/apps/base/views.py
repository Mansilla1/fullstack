# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# importar modelo
from .models import Category, Book
from .forms import CategoryForm, BookForm


# index
def index(request):
    template_name = 'index.html'
    return render(request, template_name, {})

# ------------ Categorías ---------
# Listar categorías
def category_list(request):
    template_name = 'base/categories/category_list.html'

    # obtener categorias
    categories = Category.objects.filter(status=True)
    
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
    }

    return render(request, template_name, context)

# crear una nueva categoría
def category_create(request):
    template_name = 'base/categories/category_create.html'

    if request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()

            title = 'Nueva categoría guardada con éxito'
            return redirect('base:category_list')
        else:
            title = 'Error al guardar categoría'
            return redirect('base:category_list')
            
    else:
        form = CategoryForm()
        title = False

    context = {
        'form': form,
        'title': title,
    }

    return render(request, template_name, context)

# update categorua
def category_update(request, category_id):
    template_name = 'base/categories/category_update.html'

    category = Category.objects.get(id=category_id)

    if request.POST:
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            
            title = 'Nueva categoría guardada con éxito'
            return redirect('base:category_list')
        else:
            title = 'Error al guardar categoría'
            return redirect('base:category_update', category_id)
            
    else:
        form = CategoryForm(instance=category)
        title = False

    context = {
        'category': category,
        'title': title,
    }

    return render(request, template_name, context)

# detalle del libro
def category_delete(request, category_id):
    template_name = 'base/categories/category_delete.html'

    # obtener libros
    category = Category.objects.get(id=category_id)
    if request.POST:
        category.status = False
        category.save()

        # una vez "eliminada la categoría, se deberán eliminar los libros pertenecientes"
        books = Book.objects.filter(category__id=category_id)
        for book in books:
            book.status = False
            book.save()

        return redirect('base:category_list')
    
    context = {
        'category': category,
    }

    return render(request, template_name, context)

# ---------- Libros -------------------
# Listar libros
def book_list(request, category_id):
    template_name = 'base/books/book_list.html'

    # obtener libros
    if int(category_id) == 0:
        books = Book.objects.filter(status=True)
    else:
        books = Book.objects.filter(category__id=category_id, status=True)
        
    paginator = Paginator(books, 10)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
    }

    return render(request, template_name, context)

# detalle del libro
def book_detail(request, book_id):
    template_name = 'base/books/book_detail.html'

    # obtener libros
    book = Book.objects.get(id=book_id)
    
    context = {
        'book': book,
    }

    return render(request, template_name, context)

# crear un nuevo libro
def book_create(request):
    template_name = 'base/books/book_create.html'

    categories = Category.objects.filter(status=True)

    if request.POST:
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()

            title = 'Libro almacenado con éxito'
            return redirect('base:book_list', 0)
        else:
            title = 'Error al guardar libro'
            return redirect('base:book_create')
            
    else:
        form = BookForm()
        title = False

    context = {
        'form': form,
        'title': title,
        'categories': categories,
    }

    return render(request, template_name, context)

# update un nuevo libro
def book_update(request, book_id):
    template_name = 'base/books/book_update.html'

    book = Book.objects.get(id=book_id)
    categories = Category.objects.filter(status=True)

    if request.POST:
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            
            title = 'Libro almacenado con éxito'
            return redirect('base:book_list', 0)
        else:
            title = 'Error al guardar libro'
            return redirect('base:book_update', book_id)
            
    else:
        form = BookForm(instance=book)
        title = False

    context = {
        'book': book,
        'title': title,
        'categories': categories,
    }

    return render(request, template_name, context)

# detalle del libro
def book_delete(request, book_id):
    template_name = 'base/books/book_delete.html'

    # obtener libros
    book = Book.objects.get(id=book_id)
    if request.POST:
        book.status = False
        book.save()

        return redirect('base:book_list', 0)
    
    context = {
        'book': book,
    }

    return render(request, template_name, context)