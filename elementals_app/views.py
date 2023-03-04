from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Wizard, ElementTile
from .forms import GameForm, ImageUploadForm, ElementImageUploadForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        element_images = ElementTile.objects.all()
        wizard_images = Wizard.objects.all()

        context['element_images'] = element_images
        context['wizard_images'] = wizard_images
        print(f"hej hej ")
        print(context)


class GameView(FormView):
    template_name = 'game.html'
    form_class = GameForm
    success_url = reverse_lazy('game')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wizards'] = Wizard.objects.all()
        context['elements'] = ElementTile.objects.all()
        return context

    def form_valid(self, form):
        # get selected elements from the form
        selected_elements = form.cleaned_data.get('selected_elements')

        # do something with the selected elements here, such as updating the game state or player's hand
        # still to work

        # return success response
        return super().form_valid(form)


class ImageUploadView(FormView):
    template_name = 'upload_images.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("elementals_app:index")


class ElementImageUploadView(FormView):
    template_name = 'upload_images.html'
    form_class = ElementImageUploadForm

    def get_success_url(self):
        return reverse_lazy("elementals_app:index")


