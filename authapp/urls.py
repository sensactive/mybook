from django.urls import path
from django.urls.conf import path

from authapp.views import loginView, logout

app_name = 'authapp'

urlpatterns = [
    path('', loginView, name='login'),
    path('logout/', logout, name='logout'),
]