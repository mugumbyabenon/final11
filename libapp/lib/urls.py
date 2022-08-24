from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns =[
    path('register/', views.database),
    path('database/', views.existing),
    path('librarain/database/', views.existings),
    path('search/', views.search_book),
    path('', views.home, name='home'),
    path('remove/<int:Book_number>', views.delete, name= 'rem'),
    path('borrow/<int:Book_number>', views.borrow),
    path('borrowed/', views.borrowed),
    path('books/', views.books),
    path('return/', views.check_return),
    path('returns/<username>/<int:q>/<int:book_number>', views.returns),
    path('myborrows/', views.myborrows),
    path('searchs/', views.search_book),
    path('bookdetails/<int:Book_number>', views.book_details),
    path(r'^search_b/', views.search_book, name="search_b"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)