from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.views.generic import View
from accounts.forms import LoginForm, RegisterForm, DetailsForm


class LoginView(View):
    context = {}
    template = "account/login.html"
    def get(self, request):
        self.context['loginform'] = LoginForm()
        return render(request, self.template, self.context)

    def post(self, request):
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            user = authenticate(username=loginform.cleaned_data['username'], password=loginform.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Inloggen gelukt!")
                    return redirect("events:index")
                else:
                    messages.error(request, "Deze account is niet geactiveerd")
                    return self.get(request)
            else:
                messages.warning(request, "Gebruikersnaam of wachtwoord klopt niet")
                return self.get(request)

        else:
            self.context['loginform'] = loginform
            return render(request, self.template, self.context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Uitloggen is gelukt!")

        return redirect("account:login")

class CreateNewAccountView(View):
    def get(self, request):
        context = {}

        context['registerform'] = RegisterForm()
        return render(request, "account/new.html",context)

    def post(self, request):
        registerform = RegisterForm(request.POST)
        
        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            email = registerform.cleaned_data['email']
            password = registerform.cleaned_data['password']
            password_conf = registerform.cleaned_data['password_repeat']

    
            if password != password_conf:
                messages.error(request, "De wachtwoorden kwamen niet overeen")
                return self.get(request)
    
            User.objects._create_user(username=username, password=password, email=email, is_staff=False, is_superuser=False)

            user = User.objects.get(username=username)

            user.first_name = registerform.cleaned_data['first_name']
            user.last_name = registerform.cleaned_data['last_name']

            user.save()
    
            if user.pk != None:
                messages.success(request, "Account aangemaakt!")
            else:
                messages.error(request, "Account niet aangemaakt")
    
            return redirect("events:index")
        else:
            context = {'registerform' : registerform}

            return render(request, "account/new.html", context)

class ProfileView(View):
    def get(self, request, username=None):
        context = {}

        if username== None:
            context['user'] = request.user
            context['detailsform'] = DetailsForm(instance=request.user.details)
        else:
            context['user'] = User.objects.filter(username=username)

        return render(request, "account/profile.html", context)