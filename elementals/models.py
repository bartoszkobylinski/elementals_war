from django.db import models


class ElementTile(models.Model):
    element_type = models.CharField(max_length=40)
    face_up = models.BooleanField(default=False)


class Wizard(models.Model):
    wizard_type = models.CharField(max_length=40)
    collected = models.BooleanField(default=False)


class Player(models.Model):
    name = models.CharField(max_length=50)
    wizards = models.ManyToManyField(Wizard)


class Board(models.Model):
    element_tiles = models.ManyToManyField(ElementTile)


class Game(models.Model):
    players = models.ManyToManyField(Player)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
