from django.urls import path
from .views import Login, Register, logout_user
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', Login.as_view(), name='login_url'),
    path('register/', Register.as_view(), name='register_url'),
    path('logout/', login_required(logout_user), name='logout_url'),
]
