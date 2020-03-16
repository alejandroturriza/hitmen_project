from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

TYPE_USER_CHOICES = (
    (1, 'hitman'),
    (2, 'manager')
)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control format-input'}),
        }


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
