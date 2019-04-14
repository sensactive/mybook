import requests
from django.contrib import auth
from django.shortcuts import render

# Create your views here.
from http.cookies import SimpleCookie

from authapp.forms import MyBookUserLoginForm
from authapp.models import MyBookUser


def loginView(request):
    if request.method == 'POST':
        mybookUrlAuth = 'https://mybook.ru/api/auth/'
        login_form = MyBookUserLoginForm(data=request.POST)
        if login_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            context = {
                'email': email,
                'password': password
            }
            response = requests.post(mybookUrlAuth, context)  #аутентификация на MyBook.ru
            if response.status_code == 200:
                cooks = response.headers['Set-Cookie']
                cookie = SimpleCookie() #куки из ответа сервера
                cookie.load(cooks)
                sessionCookie = cookie['session'].OutputString()  #получаем строку сессионной куки
                if auth.authenticate(username=email, password=password):
                    result = requests.get('https://mybook.ru/api/bookuserlist/', headers={
                        'cookie': sessionCookie,
                        'accept': 'application/json; version=5'
                    })
                    objects = result.json()['objects']
                    books = [b['book'] for b in objects]
                    return render(request, 'userbooks/booksList.html')
                else:
                    # создаем нового пользователя в базе
                    newUser = MyBookUser(username=email, password=password, email=email, sessionCookie=sessionCookie)
                    newUser.save()
                    auth.login(request, newUser, backend='django.contrib.auth.backends.ModelBackend') #логинимся


                result = requests.get('https://mybook.ru/api/bookuserlist/', headers={
                    'cookie': sessionCookie,
                    'accept': 'application/json; version=5'
                })
            # cooks = response.headers['Set-Cookie'] # куки из ответа сервера
            # cookie = SimpleCookie()
            # cookie.load(cooks)
            # sessionCookie = cookie['session'].OutputString() # получаем строку сессионной куки
            # request.session['mybookSession'] = sessionCookie
            # result = requests.get('https://mybook.ru/api/bookuserlist/', headers={
            #     'cookie': request.session['mybookSession'],
            #     'accept': 'application/json; version=5'
            # })
            print(result.json())
            return render(request, 'userbooks/index.html')
        else:
            content = {
                'err': 'введите правильное имя пользователя или пароль'
            }
            return render(request, 'userbooks/index.html', content)
    else:
        # for c in request.__dict__:
        #     print (c)
        # print(request.__dict__)
        print(request.COOKIES)
    return render(request, 'userbooks/index.html')