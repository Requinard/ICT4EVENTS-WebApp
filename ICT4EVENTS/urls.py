"""ICT4EVENTS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from ICT4EVENTS import settings

urlpatterns = [
    url(r'^sharing/',include("sharing.urls",namespace="sharing")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include("social.apps.django_app.urls", namespace="social")),
    url(r'^account/', include('accounts.urls', namespace="account")),
    url(r'^api/', include("api.urls", namespace='api')),
    url(r'^reservations/', include('reservations.urls', namespace="reservations")),
    url(r'^', include('events.urls', namespace="events")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
