import random
import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Element, Entity, Player
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
        # Fetch the player instance (you can change this to fetch the correct player)
        player = Player.objects.first()

        # Serialize the player
        serialized_player = serializers.serialize('json', [player], fields=('name', 'hand'))
        serialized_player = json.loads(serialized_player)[0]

        # Serialize the player's hand
        serialized_hand = serializers.serialize('json', player.hand.all(), fields=('id', 'element_type', 'image'))
        serialized_hand = json.loads(serialized_hand)

        # Add the full image URL to the player's hand elements
        for element, serialized_element in zip(player.hand.all(), serialized_hand):
            serialized_element['fields']['image'] = request.build_absolute_uri(element.image.url)

        # Update the player object with the serialized hand
        serialized_player['fields']['hand'] = serialized_hand

        # Fetch the elements for the board
        elements = list(Element.objects.all())
        board_elements = random.choices(elements, k=9)
        random.shuffle(board_elements)

        # Serialize the board elements
        serialized_elements = serializers.serialize('json', board_elements, fields=('id', 'element_type', 'image'))
        serialized_board = json.loads(serialized_elements)

        # Add the full image URL to the board elements
        for element, serialized_element in zip(board_elements, serialized_board):
            serialized_element['fields']['image'] = request.build_absolute_uri(element.image.url)

        # Reconstruct the board
        serialized_board = [serialized_board[index:index + 3] for index in range(0, 9, 3)]

        return JsonResponse({'board': serialized_board, 'player': serialized_player})

class UpdateHandView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        player_id = data.get('player_id')
        new_element_id = data.get('element_id')
        if not (player_id and new_element_id):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

        player = Player.objects.get(pk=player_id)
        new_element = Element.objects.get(pk=new_element_id)
        player.hand.add(new_element)
        player.save()
        return JsonResponse({"status": "success", 'message': "Hand updated"})

