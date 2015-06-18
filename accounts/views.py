from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import View
from accounts.forms import LoginForm, RegisterForm, DetailsForm, UserForm, SettingsForm, ActivateForm
from accounts.models import Account


class LoginView(View):
    context = {}
    template = "account/login.html"
    def get(self, request):
        if request.user.is_active:
            messages.warning(request, "you are already logged in")
            return redirect("events:index")

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
    @method_decorator(login_required)
    def get(self, request, username=None, mode=None):
        context = {}

        if username== None:
            context['requested_user'] = request.user
            context['detailsform'] = DetailsForm(instance=request.user.details)
            context['userform'] = UserForm(instance=request.user)
            context['settingsform'] = SettingsForm(instance=request.user.settings)
        else:
            context['requested_user'] = get_object_or_404(User, username=username)

        return render(request, "account/profile.html", context)

    @method_decorator(login_required)
    def post(self, request, username=None, mode=None):
        context = {}

        if username is not None:
            return self.get(request, username, mode)

        context['detailsform'] = DetailsForm(instance=request.user.details)
        context['userform'] = UserForm(instance=request.user)
        context['settingsform'] = SettingsForm(instance=request.user.settings)

        if mode == "details":
            form = DetailsForm(request.POST, instance=request.user.details)

            if form.is_valid():
                form.save()
                messages.success(request, "Persoonsgegevens veranderd")
                return self.get(request)
            else:
                messages.warning(request, "Er zijn een paar velden niet goed ingevuld")
                context['detailsform'] = form

        elif mode == "profile":
            user = UserForm(request.POST, instance=request.user)

            if user.is_valid():
                user.save()
                messages.success(request, "Profiel opgeslagen!")
                return self.get(request)
            else:
                messages.warning(request, "Er zijn een paar velden niet goed ingevuld")
                context['userform'] = user

        elif mode == "settings":
            settings = SettingsForm(request.POST, request.FILES, instance=request.user.settings)

            if settings.is_valid():
                settings.save()
                messages.success(request,"Intelling gewijzigd")
                return self.get(request)
            else:
                messages.warning(request, "Er zijn een paar velden niet goed ingevuld")
                context['settingsform'] = settings

        return render(request, "account/profile.html", context)

class ActivateView(View):
    def get(self, request, hashcode):
        context = {}
        user = Account.objects.get(activatiehash=hashcode).gebruiker

        if user.is_active:
            messages.error(request, "This account has already been activated!")
            return redirect("account:login")

        context['form'] = ActivateForm(instance=user)

        return render(request, "account/activate.html", context)

    def post(self, request, hashcode):
        context = {}
        user = Account.objects.get(activatiehash=hashcode).gebruiker

        if user.is_active:
            messages.error(request, "This account has already been activated!")
            return redirect("account:login")

        form = ActivateForm(request.POST, instance=user)

        if form.is_valid():
            new_user = form.save(commit=False)

            new_user.is_active = True
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            messages.success(request, "Account was succesfully activated!")
            return redirect("account:login")

        context['form'] = form

        return render(request, "account/activate.html", context)


