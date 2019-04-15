from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from http.cookies import SimpleCookie

# from .forms import MyBoookUserForm

# Create your views here.


# def mainView(request):
#     if request.method == 'POST':
#         mybookUrlAuth = 'https://mybook.ru/api/auth/'
#         context = {
#             'email': request.POST['email'],
#             'password': request.POST['password']
#         }
#         response = requests.post(mybookUrlAuth, context) # аутентификация
#         if response.status_code == 200:
#             cooks = response.headers['Set-Cookie'] # куки из ответа сервера
#             cookie = SimpleCookie()
#             cookie.load(cooks)
#             sessionCookie = cookie['session'].OutputString() # получаем строку сессионной куки
#             request.session['mybookSession'] = sessionCookie
#             result = requests.get('https://mybook.ru/api/bookuserlist/', headers={
#                 'cookie': request.session['mybookSession'],
#                 'accept': 'application/json; version=5'
#             })
#             print(result.json())
#             return render(request, 'userbooks/index.html')
#         else:
#             content = {
#                 'err': 'введите правильное имя пользователя или пароль'
#             }
#             return render(request, 'userbooks/index.html', content)
#     else:
#         # for c in request.__dict__:
#         #     print (c)
#         # print(request.__dict__)
#         print(request.COOKIES)
#     return render(request, 'userbooks/index.html')