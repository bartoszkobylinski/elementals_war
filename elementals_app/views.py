from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Wizard, ElementTile
from .forms import GameForm, ImageUploadForm, ElementImageUploadForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        element_images = ElementTile.objects.all()
        wizard_images = Wizard.objects.all()

        context['element_images'] = element_images
        context['wizard_images'] = wizard_images
        print(f"hej hej ")
        for x in context['wizard_images']:
            print(x.image.url)


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


class ImageUploadView(View):
    def get(self, request):
        return render(request, 'upload_images.html')

    def post(self, request):
        print(request)
        image_file = request.FILES['image_file']
        image_type = request.POST['image_type']
        if settings.USE_S3:
            print("I have used S3 stetting")
            if image_type == 'element_tile':
                obj = ElementTile(image=image_file)
            elif image_type == 'wizard':
                obj = Wizard(image=image_file)
            obj.save()
            image_url = obj.image.url
        else:
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_url = fs.url(filename)
        return render(request, 'upload_images.html', {
            'image_url': image_url
        })


class ElementImageUploadView(FormView):
    template_name = 'upload_images.html'
    form_class = ElementImageUploadForm

    def get_success_url(self):
        return reverse_lazy("elementals_app:index")
