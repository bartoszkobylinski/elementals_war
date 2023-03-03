from django.db import models


class ElementTile(models.Model):
    element_type = models.CharField(max_length=40)
    face_up = models.BooleanField(default=False)


class Wizard(models.Model):
    wizard_type = models.CharField(max_length=40)
    collected = models.BooleanField(default=False)
    image = models.ImageField(upload_to='wizard_images/', blank=True, null=True)


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
