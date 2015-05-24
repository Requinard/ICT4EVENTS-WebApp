from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.views.generic import View


class LoginView(View):
    context = {}
    template = "account/login.html"
    def get(self, request):
        return render(request, self.template, self.context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
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

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Uitloggen is gelukt!")

        return redirect("account:login")


class MagicView(View):
    def get(self, request):
        context = {}

        context['dummy_user'] = User.objects.get(id=1)

        return render(request, 'account/dummy.html', context)