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
        print(element_images)
        entity_images = Entity.objects.all()
        print(entity_images)

        context['element_images'] = element_images
        context['wizard_images'] = entity_images
        for x in context['wizard_images']:
            print(x.image.url)


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
