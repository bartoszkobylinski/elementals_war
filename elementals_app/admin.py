from django.contrib import admin
from .models import Entity, Element, Player

admin.site.register(Player)
admin.site.register(Entity)
admin.site.register(Element)

