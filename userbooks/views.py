from django.shortcuts import render
import requests


# Create your views here.


def mainView(request):
    mybookUrlAuth = 'https://mybook.ru/api/auth/'
    context = {
        'email': 'sensor14@list.ru',
        'password': '4606441241Aa'
    }
    response = requests.post(mybookUrlAuth, context)
    # print(response.headers)
    cookies = response.headers['Set-Cookie']

    return render(request, 'userbooks/index.html')