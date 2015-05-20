from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        messages.success(request, "Messages werken!")
        messages.warning(request, "Er ging iets fout")
        messages.error(request, "dit is een error")
        return render(request, 'base.html', {})