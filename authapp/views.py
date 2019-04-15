import requests
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from http.cookies import SimpleCookie

from authapp.forms import MyBookUserLoginForm
from authapp.models import MyBookUser


def loginView(request):
    if request.user.is_authenticated:
        print(request.user.sessionCookie)
        books = getBooksList(request.user.sessionCookie)
        content = {
            'books': books
        }
        return render(request, 'userbooks/booksList.html', content)
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        mybookUrlAuth = 'https://mybook.ru/api/auth/'
        user = auth.authenticate(username=email, password=password)
        if user:
            context = {
                'email': email,
                'password': password
            }
            response = requests.post(mybookUrlAuth, context)  #аутентификация на MyBook.ru
            if response.status_code == 200:
                cooks = response.headers['Set-Cookie']
                cookie = SimpleCookie() #куки из ответа сервера
                cookie.load(cooks)
                u = MyBookUser.objects.get(pk=user.pk)
                u.sessionCookie = cookie['session'].OutputString() #пишем строку сессионной куки пользователю
                u.save()
                auth.login(request, u, backend='django.contrib.auth.backends.ModelBackend')
                books = getBooksList(u.sessionCookie)
                content = {
                    'books': books,
                    'user': u
                }
            else:
                auth.logout(request)
                content = {
                    'err': 'Вы не зарегистрированы на MyBook.ru'
                }
            return render(request, 'userbooks/booksList.html', content)
        else:
            # создаем нового пользователя в базе
            newUser = MyBookUser.objects.create_user(username=email, password=password, email=email)
            newUser.save()
            auth.login(request, newUser, backend='django.contrib.auth.backends.ModelBackend') #логинимся
            return render(request, 'userbooks/booksList.html')
    return render(request, 'userbooks/index.html')

def getBooksList(usersCookie):
    result = requests.get('https://mybook.ru/api/bookuserlist/', headers={
        'cookie': usersCookie,
        'accept': 'application/json; version=5'
    })
    print(result.json()['meta'])
    objects = result.json()['objects']
    books = [b['book'] for b in objects]
    return books

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))