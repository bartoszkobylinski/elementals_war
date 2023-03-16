import random

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Element, Entity
from .forms import ImageForm
from django.utils import timezone


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        element_images = Element.objects.all()
        entity_images = Entity.objects.all()
        context['element_images'] = element_images
        context['entity_images'] = entity_images
        return context


class GameView(TemplateView):
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        element_images = Element.objects.all()
        entity_images = Entity.objects.all()
        context['element_images'] = element_images
        context['entity_images'] = entity_images
        return context

class ImageUploadView(View):
    form_class = ImageForm
    template_name = 'image_upload.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            element_images = request.FILES.getlist('element_images')
            entity_images = request.FILES.getlist('entity_images')
            element_type = form.cleaned_data['element_type']
            entity_type = form.cleaned_data['entity_type']
            for image in element_images:
                obj = Element(element_type=element_type, image=image)
                obj.uploaded_at = timezone.now()
                obj.save()
            for image in entity_images:
                obj = Entity(entity_type=entity_type, image=image)
                obj.uploaded_at = timezone.now()
                obj.save()
            #  later add successful redirect
            form = self.form_class()
        return render(request, self.template_name, {'form': form})


class VueAppView(View):
    def get(self, request, *args, **kwargs):
        elements = Element.objects.all()
        entities = Entity.objects.all()
        data = {
            'elements': [{'element_type': e.element_type, 'image_url': e.image.url} for e in elements],
            'entities': [{'entity_type': e.entity_type, 'image_url': e.image.url} for e in entities]
        }
        return JsonResponse(data)


class ElementalsWarView(View):
    def get(self, request, *args, **kwargs):
        elements = list(Element.objects.values('id', 'element_type', 'image'))
        random.shuffle(elements)
        elements = elements[:9]
        board = [elements[index:index+3] for index in range(0, 9, 3)]
        return JsonResponse({'board': board})
