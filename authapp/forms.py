from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import MyBookUser

class MyBookUserLoginForm(AuthenticationForm):

    class Meta:
        model = MyBookUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(MyBookUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'