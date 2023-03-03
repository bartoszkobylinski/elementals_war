from django.urls import path
from .views import IndexView, GameView

app_name = 'elementals_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('game/', GameView.as_view(), name='game'),
]