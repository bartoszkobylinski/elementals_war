from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils import timezone


class ElementTile(models.Model):
    element_type = models.CharField(max_length=40)
    face_up = models.BooleanField(default=False)
    image = models.ImageField(upload_to='element_images/', blank=True, null=True)

    def __str__(self):
        if self.image:
            return f"{self.element_type} ({self.image.url})"
        else:
            return self.element_type


class Wizard(models.Model):
    wizard_type = models.CharField(max_length=40)
    collected = models.BooleanField(default=False)
    image = models.ImageField(upload_to='wizard_images/', blank=True, null=True)

    def __str__(self):
        if self.image:
            return f"{self.wizard_type} ({self.image.url})"
        else:
            return self.wizard_type


class Player(models.Model):
    name = models.CharField(max_length=50)
    wizards = models.ManyToManyField(Wizard)


class Board(models.Model):
    element_tiles = models.ManyToManyField(ElementTile)


class Game(models.Model):
    players = models.ManyToManyField(Player, related_name='games_played')
    wizards = models.ManyToManyField(Wizard)
    elements = models.ManyToManyField(ElementTile)
    winner = models.ForeignKey(Player, related_name='games_won', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Game {self.id}'


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

