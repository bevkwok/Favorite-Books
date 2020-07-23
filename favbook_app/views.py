from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_pw)
        request.session['user_id'] = new_user.id
        messages.success(request, "User created!", extra_tags='register')
        return redirect('/')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    search_user = User.objects.filter(email = email)
    if len(search_user) > 0:
        login_user = search_user[0]
        if bcrypt.checkpw(password.encode(), login_user.password.encode()):
            request.session['user_id'] = login_user.id
            return redirect('/books')
        else:
            messages.error(request, "Incorrect password", extra_tags='login')
            return redirect('/')
    else:
        messages.error(request, "This email has not been registered", extra_tags='login')
        return redirect('/')

def main(request):
    if not "user_id" in request.session:
        messages.error(request, "Please login", extra_tags='login')
        return redirect('/')
    context = {
            "user" : User.objects.get(id = request.session['user_id']),
            "book" : Book.objects.exclude(fav=User.objects.get(id = request.session['user_id']))
            }
    return render(request,"main.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add_book(request):
    if len(request.POST['title']) <= 0:
        messages.error(request, "Please enter title for book", extra_tags="book")
        return redirect('/books')
    if len(request.POST['desc']) < 5:
        messages.error(request, "Descroption must be at least 5 characters", extra_tags="book")
        return redirect('/books')
    else:
        title= request.POST.get('title')
        desc = request.POST.get('desc')
        user = User.objects.get(id = request.session['user_id'])
        new_book = Book.objects.create(title=title, desc=desc, uploaded_by=user)
        new_book.save()
        new_book.fav.add(user)
        return redirect('/books')

def add_fav(request):
    hidden_book_id = request.POST.get('hidden_fav')
    user = User.objects.get(id = request.session['user_id'])
    the_book = Book.objects.get(id=request.POST.get('hidden_fav'))
    the_book.fav.add(user)
    return redirect('/books')

def show_book(request, id):
    context = {
        "get_book" : Book.objects.get(id=id),
        "user" : User.objects.get(id = request.session['user_id']),
    }
    return render(request, "show_book.html", context)

def edit_book(request):
    book_id = request.POST.get('hidden_book_id')
    title= request.POST.get('title')
    desc = request.POST.get('desc')

    # if len(title) < 1:
    #     messages.error(request, "Please enter title for book", extra_tags="book")
    #     return redirect('/books/'+ book_id)
    # if len(desc) < 5:
    #     messages.error(request, "Descroption must be at least 5 characters", extra_tags="book")
    #     return redirect('/books/' + book_id)
    # else:
    update_book = Book.objects.get(id=request.POST.get('hidden_book_id'))
    update_book.title = request.POST.get('title')
    update_book.desc = request.POST.get('desc')
    print(request.POST.get('title'))
    print(request.POST.get('desc'))
    update_book.save()
    return redirect('/books/' + book_id)


def del_book(request):
    book_id = request.POST.get('hidden_book_id')
    return redirect('/books/' + book_id)

def unfav(request):
    book_id = request.POST.get('hidden_book_id')
    user_id = request.session['user_id']
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=user_id)
    this_book.fav.remove(this_user)
    return redirect('/books/' + book_id)

def fav(request):
    book_id = request.POST.get('hidden_book_id')
    user_id = request.session['user_id']
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=user_id)
    this_book.fav.add(this_user)
    return redirect('/books/' + book_id)