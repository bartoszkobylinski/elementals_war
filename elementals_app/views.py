import random
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .models import Element, Entity, Player
from .forms import ImageForm
from django.utils import timezone
from helpers import serialize_board


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
        player = Player.objects.first()
        serialized_player = player.serialize(request)

        if cache.get('stack'):
            stack = cache.get('stack')
        else:
            stack = [element for _ in range(7) for element in Element.objects.all()]
            cache.set('stack', stack)

        if len(stack) >= 9:
            board_elements = random.sample(stack, k=9)
            stack = [element for element in stack if element not in board_elements]
        else:
            board_elements = [Element.objects.filter(element_type='empty').first() for _ in range(9)]

        serialized_board = serialize_board(board_elements, request)
        cache.set('stack', stack)

        return JsonResponse({'board': serialized_board, 'player': serialized_player})


class UpdateHandView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            player_id = data.get('player_id')
            new_element_id = data.get('element_id')
            print(f"this is data: {data}")
            if not (player_id and new_element_id):
                return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

            player = Player.objects.get(pk=player_id)
            new_element = Element.objects.get(pk=new_element_id)
            player.hand.add(new_element)
            player.save()
            return JsonResponse({"status": "success", 'message': "Hand updated"})
        except (ValueError, KeyError, Player.DoesNotExist, Element.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)


class ClearHandView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            player_id = data.get('player_id')
            print(f"to jest player_id: {player_id}")
            if not player_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

            player = Player.objects.get(pk=player_id)
            player.hand.clear()
            player.save()
            return JsonResponse({'status': 'success', 'message': 'Hand cleared'})
        except (ValueError, KeyError, Player.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
