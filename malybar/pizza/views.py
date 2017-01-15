# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import models
from . import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


def index(request):
    """Strona główna"""
    kontekst = {'komunikat': 'Witaj w aplikacji Pizza!'}
    return render(request, 'pizza/index.html', kontekst)


def kontakt(request):
    """Strona główna"""
    kontekst = {'kontakt': ' budynek 0'}
    return render(request, 'pizza/kontakt.html', kontekst)


@method_decorator(login_required, 'dispatch')
class PizzaCreate(CreateView):
    """Widok dodawania pizzy i skladników."""
    model = models.Pizza
    form_class = forms.PizzaForm
    success_url = reverse_lazy('pizza:lista')  # '/pizza/lista'

    def get_context_data(self, **kwargs):
        context = super(PizzaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['skladniki'] = forms.SkladnikiFormSet(self.request.POST)
        else:
            context['skladniki'] = forms.SkladnikiFormSet()
            context['imie'] = 'jan pikula'  # dod elem w form pizza_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        skladniki = forms.SkladnikiFormSet(self.request.POST)
        if form.is_valid() and skladniki.is_valid():
            return self.form_valid(form, skladniki)
        else:
            return self.form_invalid(form, skladniki)

    def form_valid(self, form, skladniki):
        form.instance.autor = self.request.user
        self.object = form.save()
        skladniki.instance = self.object
        skladniki.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, skladniki):
        return self.render_to_response(
            self.get_context_data(form=form, skladniki=skladniki)
        )


@method_decorator(login_required, 'dispatch')
class PizzaUpdate(UpdateView):
    """Widok aktualizuacji"""

    model = models.Pizza
    form_class = forms.PizzaForm
    success_url = reverse_lazy('pizza:lista')  # '/pizza/lista'

    def get_context_data(self, **kwargs):
        context = super(PizzaUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['skladniki'] = forms.SkladnikiFormSet(
                self.request.POST,
                instance=self.object)
        else:
            context['skladniki'] = forms.SkladnikiFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        skladniki = forms.SkladnikiFormSet(
            self.request.POST,
            instance=self.object)
        if form.is_valid() and skladniki.is_valid():
            return self.form_valid(form, skladniki)
        else:
            return self.form_invalid(form, skladniki)

    def form_valid(self, form, skladniki):
        form.instance.autor = self.request.user
        self.object = form.save()
        skladniki.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, skladniki):
        return self.render_to_response(
            self.get_context_data(form=form, skladniki=skladniki)
        )


@method_decorator(login_required, 'dispatch')
class PizzaDelete(DeleteView):
    model = models.Pizza
    success_url = reverse_lazy('pizza:lista')  # '/pizza/lista'

    def get_context_data(self, **kwargs):
        context = super(PizzaDelete, self).get_context_data(**kwargs)
        skladniki = models.Skladnik.objects.filter(pizza=self.object)
        context['skladniki'] = skladniki
        return context
