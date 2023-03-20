import json
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils import timezone
from django.core import serializers


class Element(models.Model):
    ELEMENT_TYPES = (
        ('Earth', 'Earth'),
        ('Air', 'Air'),
        ('Darkness', 'Darkness'),
        ('Fire', 'Fire'),
        ('Lightning', 'Lightning'),
        ('Water', 'Water')
    )
    element_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
    image = models.ImageField(storage=S3Boto3Storage())
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.element_type} element."


class Entity(models.Model):
    ELEMENT_TYPES = (
        ('Earth', 'Earth'),
        ('Air', 'Air'),
        ('Darkness', 'Darkness'),
        ('Fire', 'Fire'),
        ('Lightning', 'Lightning'),
        ('Water', 'Water')
    )
    entity_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
    image = models.ImageField(storage=S3Boto3Storage())
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.entity_type} entity."


class Player(models.Model):
    name = models.CharField(max_length=100)
    hand = models.ManyToManyField(Element, blank=True, related_name='players_holding')
    entities = models.ManyToManyField(Entity, blank=True)

    def __str__(self):
        return self.name

    def serialize(self, request):
        # Serialize the player
        serialized_player = serializers.serialize('json', [self], fields=('name', 'hand'))
        serialized_player = json.loads(serialized_player)[0]

        # Serialize the player's hand
        serialized_hand = serializers.serialize('json', self.hand.all(), fields=('id', 'element_type', 'image'))
        serialized_hand = json.loads(serialized_hand)

        # Add the full image URL to the player's hand elements
        for element, serialized_element in zip(self.hand.all(), serialized_hand):
            serialized_element['fields']['image'] = request.build_absolute_uri(element.image.url)

        # Update the player object with the serialized hand
        serialized_player['fields']['hand'] = serialized_hand

        # Serialize the player's entities
        serialized_entities = serializers.serialize('json', self.entities.all(), fields=('id', 'entity_type', 'image'))
        serialized_entities = json.loads(serialized_entities)

        # Add the full image URL to the player's entity elements
        for entity, serialized_entity in zip(self.entities.all(), serialized_entities):
            serialized_entity['fields']['image'] = request.build_absolute_uri(entity.image.url)

        # Update the player object with the serialized entities
        serialized_player['fields']['entities'] = serialized_entities

        return serialized_player
