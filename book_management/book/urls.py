from django.urls import path 
from . import views

urlpatterns = [
    path('',views.list_books, name='list_book'),
    path('add_book/',views.add_book , name='add_book'),
    path('list_books/',views.list_books , name='list_books'),
    path('update_book/<int:book_id>/', views.update_book, name='update_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    path('list_authors/',views.list_authors , name='list_authors'),
]
