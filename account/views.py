from django.shortcuts import render, redirect
from django import views
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import Hitman


class Login(views.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('hits_url')
        else:
            form = LoginForm()
            return render(request, 'login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # get credentials
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # verify user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hits_url')
        messages.error(request, 'Your username or password was incorrect.', extra_tags='danger')
        return render(request, 'login.html', context={'form': form})


class Register(views.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('hits_url')
        else:
            form = CreateUserForm()
            return render(request, 'register.html', context={'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if request.POST['user_type'] == 'hitman':
                hitman = Hitman()
                hitman.user = new_user
                hitman.description = request.POST['description_hitman']
                hitman.save()
                messages.success(request, 'Hitman created successfuly')
            else:
                new_user.is_staff = True
                new_user.save()
                messages.success(request, 'Manager created successfuly')
        return render(request, 'register.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('login_url')
