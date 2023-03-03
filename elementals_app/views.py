from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Wizard, ElementTile
from .forms import GameForm


class IndexView(TemplateView):
    template_name = 'index.html'


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

class UploadWizardImage(View):
    def get(self, request):
        form = WizardImageForm()
        wizards = Wizard.objects.all()
        return render(request, 'upload_wizard_image.html', {'form': form, 'wizards': wizards})

    def post(self, request):
        form = WizardImageForm(request.POST, request.FILES)
        if form.is_valid():
            wizard_id = form.cleaned_data['wizard_id']
            wizard = Wizard.objects.get(id=wizard_id)
            wizard.image = form.cleaned_data['image']
            wizard.save()
        return redirect('upload_wizard_image')
