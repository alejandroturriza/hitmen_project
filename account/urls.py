from django.urls import path
from .views import Login, Register, logout_user

urlpatterns = [
    path('login/', Login.as_view(), name='login_url'),
    path('register/', Register.as_view(), name='register_url'),
    path('logout/', logout_user, name='logout_url'),
]
