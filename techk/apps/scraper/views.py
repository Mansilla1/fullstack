# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup
import apps.scraper.config as configuracion

# importar models
from apps.base.models import Category, Book


# metodos de scraping
'''  Almacenar categorias en la base de datos
entrada: url "padre"
salida: almacena categorias en la base de datos
'''
def get_categories(url):
    req = requests.get(url)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html.parser")
    data = soup.find('ul', 'nav nav-list').findNext('li').findNext('ul').find_all('li')
    # crear categorias
    for i, category in enumerate(data):
        category_name = ' '.join(category.find('a').text.split()).capitalize()
        if len(Category.objects.filter(name=category_name)) <= 0:
            Category.objects.create(name=category_name)

    print('Se registraron {} categorías'.format(i+1))

''' Obtener las url de cada libro
entrada: url "padre"
retorna: lista de urls a recorrer
'''
def get_books_url(url):
    req = requests.get(url)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html.parser")
    # obtener todos los libros de la página (incluye paginación)
    cant_pages = int(soup.select('ul.pager > li.current')[0].text.split()[-1]) # obtener el numero total
    # recorrer todas las url por páginas y obtener las url a recorrer para obtener la data asociada a book
    books_url = []
    for page in range(1,cant_pages+1):
        url_page = '{}/catalogue/page-{}.html'.format(url, page)
        req = requests.get(url_page)
        soup = BeautifulSoup(req.text, "html.parser")
        for article in soup.find_all('article'):
            books_url.append('{}/catalogue/{}'.format(url, article.h3.a.get('href')))
    print('Se registraron {} libros'.format(len(books_url)))
    return books_url



# Create your views here.

def scraping_create(request):
    template_name = 'scraper/scraping_create.html'
    # obtener url padre

    if request.POST:
        url = request.POST['url']
        # obtener categorías desde la página de inicio
        get_categories(url)
        
        # obtener todas las urls a recorrer (por libro)
        books_url = get_books_url(url)

        # recorrer cada pagina para obtener la info del libro
        print('Recolectar datos de los libros')
        for book in books_url:
            print(book)
            req = requests.get(book)
            req.encoding = 'utf-8'
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html.parser")
                # obtener la data
                title = soup.h1.text
                price = soup.find('p','price_color').text
                upc = soup.find(text='UPC').findNext('td').text
                stock = True if 'in stock' in soup.find(text='Availability').findNext('td').text.lower() else False
                try:
                    thumbnail = '{}/{}'.format(url, soup.img.get('src').split('../')[-1]) # url de la imagen
                    product_description = soup.find(id='product_description').findNext('p').text
                except:
                    thumbnail = None
                    product_description = None
                # buscar categoria
                category_name = ' '.join(soup.find('ul', 'breadcrumb').find_all('li')[-2].text.split()).capitalize()
                try: # si no existe, se crea una
                    category = Category.objects.get(name=category_name)
                except:
                    category = Category.objects.create(name=category_name)
                
                # ahora, ha registrar el libro en la base de datos
                if len(Book.objects.filter(title=title, price=price, upc=upc, category=category)) <= 0:
                    Book.objects.create(title=title, price=price, upc=upc, category=category, product_description=product_description,
                                thumbnail=thumbnail, stock=stock)
        
        return redirect('base:category_list')

        ''' Hacer un for hasta recorrer todas las paginas, estas salen al final (indica cuantas hay)
        Para acceder al libro, obtener el title desde la pagina principal y luego modificar la url
        '''
        context = {

        }
    else:
        context = {
            'url': configuracion.urls['url']
        }
        

    return render(request, template_name, context)

