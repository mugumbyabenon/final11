import datetime
from django.shortcuts import render,redirect
from .models import lib, borrowed_books
from .forms import libform,returnss,Sform
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import F
from django.db import IntegrityError
from accounts.models import User
from libapp import settings
from .tasks import send_notification
# Create your views here.
import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

@user_passes_test(lambda u: u.is_staff)
def database(request):
    title = 'Book Registration'
    form = libform(request.POST or None, request.FILES)
    if form.is_valid():
        name = form.cleaned_data['Book_name']
        author = form.cleaned_data['Book_author']
        category = form.cleaned_data['Book_category']
        shelf_number = form.cleaned_data['Book_shelf']
        available = form.cleaned_data['Number_of_available_copies']
        pic = form.cleaned_data['Image']
        summary = form.cleaned_data['Summary']
        p = lib(Book_name=name, Book_author=author, Book_category=category, Book_shelf=shelf_number, Number_of_available_copies=available,pic=pic,summary=summary)
        p.save()
        messages.success(request, 'Book is registered successfully')
        return redirect('/register/')
    context = {
        'title':title,
        'form':form
    }
    return render(request, 'button.html',context)
@user_passes_test(lambda u: u.is_student)
def existing(request):
    title = 'List of available books'
    queryset = lib.objects.all()
    context = {
        'title':title,
        'queryset':queryset
    }
    return render(request, 'table.html', context)
def books(request):
    title = 'List of available books'
    queryset = lib.objects.all()
    context = {
        'title': title,
        'queryset': queryset
    }
    return render(request, 'table.html', context)
def book_details(request,Book_number):
    k = lib.objects.get(Book_number=Book_number)
    return render(request, 'yeye.html',{'k':k})

def home(request):
    send_notification.delay()
    return render(request, 'temp.html')

@user_passes_test(lambda u: u.is_staff)
def existings(request):
    title = 'List of available books'
    queryset = lib.objects.all()
    context = {
        'title':title,
        'queryset':queryset
    }
    return render(request, 'books.html', context)

@user_passes_test(lambda u: u.is_staff)
def delete(request, Book_number):
    if borrowed_books.objects.filter(book_number=Book_number).exists():
        messages.success(request, 'Some copies are missing from library:You cannot delete the book')
        return redirect('/librarain/database/')
    else:
        b = lib.objects.get(Book_number=Book_number)
        lib.objects.filter(Book_number=b.Book_number).delete()
        messages.success(request, 'Book is deleted successfully')
        title = 'List of available books'
        queryset = lib.objects.all()
        context = {
            'title': title,
            'queryset': queryset
        }
        return redirect('/librarain/database/')

@user_passes_test(lambda u: u.is_student)
def borrow(request, Book_number):
    user = request.user
    if user.books_borrowed < 3:
              try:
                  book = lib.objects.get(Book_number=Book_number)
                  lib.objects.filter(Book_number=Book_number).update(Number_of_available_copies=F('Number_of_available_copies') - 1)
                  user.books_borrowed += 1
                  user.save()
              except IntegrityError:
                  messages.success(request, 'Book is out of stock')
                  return redirect('/database/')
              x = request.user.first_name
              y = request.user.last_name
              z = request.user.Reg
              r = request.user.username
              g = datetime.datetime.now()
              return_date = datetime.datetime.now() + datetime.timedelta(days=7)
              w = borrowed_books(book_title=book.Book_name, borrower_fname=x, date=g, borrower_lname=y, borrower_number=z,
                                 Return=return_date, book_number= Book_number,username=r)
              w.save()
              messages.success(request, 'Book is borrowed successfully and your return ID is in your borrowed books folder')
              return redirect('/database/')
    else:
        messages.success(request, 'Book borrow limit reached')
        return redirect('/database/')

@user_passes_test(lambda u: u.is_staff)
def borrowed(request):
    send_notification()
    title = 'List of borrowed books'
    queryset = borrowed_books.objects.all()
    x = lib.objects.all()
    context = {
        'title': title,
        'queryset': queryset,
        'x': x,
    }
    return render(request, 'borrowtable.html', context)
@user_passes_test(lambda u: u.is_staff)
def returns(request,username,q,book_number):
    y = User.objects.get(username=username)
    if y.fine == False:
        z = borrowed_books.objects.get(q=q)
        return_dates = z.Return + datetime.timedelta(days=3)
        f = z.Return + datetime.timedelta(days=10)
        if datetime.datetime.now().date() > f.date():
            y.fine = True
            y.save()
            messages.success(request, 'Please pay a fine of Shs.15000')
            User.objects.update(total=F('total') + 15000)
            return render(request,'payfine.html',{'z':z})
        elif datetime.datetime.now().date() > return_dates.date():
            y.fine = True
            y.save()
            User.objects.update(total=F('total') + 5000)
            messages.success(request, 'Please pay a fine of Shs.5000 for late return')
            return render(request, 'payfine.html',{'z':z})
        else:
            y.fine = True
            y.save()
            messages.success(request, 'No fine due return book')
            return render(request, 'payfine.html',{'z':z})
    elif y.fine ==True:
        z = borrowed_books.objects.get(q=q)
        y.fine = False
        y.save()
        lib.objects.filter(Book_number=book_number).update(Number_of_available_copies=F('Number_of_available_copies') + 1)
        User.objects.filter(username=username).update(books_borrowed=F('books_borrowed') - 1)
        borrowed_books.objects.filter(q=z.q).delete()
        messages.success(request, 'Book returned successfully')
        return redirect('/borrowed/')


@user_passes_test(lambda u: u.is_staff)
def check_return(request):
    title = 'Search for books to return'
    form = returnss(request.POST or None)
    try:
        if form.is_valid():
            name = form.cleaned_data['Return_Code']
            queryset = borrowed_books.objects.filter(q=name).all()
            return render(request, 'borrowtable.html', {'queryset':queryset})
    except ValueError:
        messages.success(request, 'Return code invalid')
        return redirect('/return/')
    context = {
            'title': title,
            'form': form,
        }
    return render(request, 'returnsearch.html', context)

@user_passes_test(lambda u: u.is_student)
def myborrows(request):
    title = 'List of borrowed books'
    queryset = borrowed_books.objects.filter(borrower_number=request.user.Reg).all()
    context = {
        'title': title,
        'queryset': queryset
    }
    return render(request, 'myborrows.html', context)

def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['Book_author', 'Book_name','Book_category'])

        book_list= lib.objects.filter(entry_query)

    return render(request,'test.html',locals() )
