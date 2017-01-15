# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views  # import widoków aplikacji
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Pizza, Skladnik


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kontakt$', views.kontakt, name='kontakt'),
    url(r'^lista/', login_required(ListView.as_view(model=Pizza)),
        name='lista'),
    url(r'^listas/', login_required(ListView.as_view(model=Skladnik)),
        name='listas'),
    url(r'^dodaj/$', views.PizzaCreate.as_view(), name='dodaj'),
]
