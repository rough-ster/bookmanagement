from django.core.paginator import Paginator
import json
from django.shortcuts import render
from .models import Author
import os
from django.http import HttpResponseRedirect
from django.urls import reverse



def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        

        # Check if all fields are filled
        if not title or not author or not description:
            return render(request, 'book/add_book.html', {'error_message': 'Please fill in all fields'})





        # Open the JSON file and add the new book to it
        if os.path.getsize('book/data/books.json') > 0:
            with open('book/data/books.json', 'r') as f:
                books = json.load(f)
        else:
            books = []

        # Generate a new primary key for the book
        book_id = len(books) + 1

        books.append({
            'id': book_id,
            'title': title,
            'author': author,
            'description': description
        })

        with open('book/data/books.json', 'w') as f:
            json.dump(books, f, indent=4)

        return HttpResponseRedirect(reverse('list_books'))

    return render(request, 'book/add_book.html')





def list_books(request):
    with open('book/data/books.json', 'r') as f:
        books = json.load(f)

    paginator = Paginator(books, 5)
    page = request.GET.get('page')

    books_on_page = paginator.get_page(page)

    return render(request, 'book/list_books.html', {'books': books_on_page})






def update_book(request, book_id):
    # Get the book with the given ID from the JSON file
    with open('book/data/books.json', 'r') as f:
        books = json.load(f)

    book = None
    for b in books:
        if b['id'] == book_id:
            book = b
            break

    if request.method == 'POST':
        # Update the book in the JSON file
        book['title'] = request.POST.get('title')
        book['author'] = request.POST.get('author')
        book['description'] = request.POST.get('description')

        with open('book/data/books.json', 'w') as f:
            json.dump(books, f, indent=4)

        return HttpResponseRedirect(reverse('list_books'))

    return render(request, 'book/update_book.html', {'book': book})



def delete_book(request, book_id):
    # Open the JSON file and remove the book with the given id
    with open('book/data/books.json', 'r') as f:
        books = json.load(f)

    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            break
    if request.method == 'POST':

        with open('book/data/books.json', 'w') as f:
            json.dump(books, f, indent=4)
        return HttpResponseRedirect(reverse('list_books'))

    return render(request, 'book/delete_book.html')










def list_authors(request):
    if os.path.getsize('book/data/books.json') > 0:
        with open('book/data/books.json', 'r') as f:
            books = json.load(f)
    else:
        books = []

    authors = set([book['author'] for book in books])
    context = {'authors': authors}
    
    return render(request, 'book/list_authors.html', context)