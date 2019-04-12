from django.urls import path
from userbooks import views as userbooks

app_name = 'userbooks'

urlpatterns = {
    path('', userbooks.mainView, name='main'),
}