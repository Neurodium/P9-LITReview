from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from reviews.models import UserFollows
from authentication.models import User
from . import forms


class LoginPage(View):
    login_form = forms.LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = self.login_form()
            message = ''
            return render(
                request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.login_form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            follow_self = UserFollows(user=user, followed_user=user)
            follow_self.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
    else:
        form = forms.RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')