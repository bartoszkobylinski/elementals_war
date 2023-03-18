from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils import timezone


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
    name = models.CharField(max_length=255)
    hand = models.ManyToManyField(Element)
    entities = models.ManyToManyField(Entity)

    def __str__(self):
        return self.name
