from django.urls import path
from .views import \
    IndexView, ImageUploadView, GameView, VueAppView, ElementalsWarView, UpdateHandView, ClearHandView, EntityImageView

app_name = 'elementals_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('upload/', ImageUploadView.as_view(), name='image_upload'),
    path('game/', GameView.as_view(), name='game'),
    path('vue_app/', VueAppView.as_view(), name='vue'),
    path('api/board/', ElementalsWarView.as_view(), name='elementals_war_board'),
    path('api/update_hand/', UpdateHandView.as_view(), name='update_hand'),
    path('api/clear_hand/', ClearHandView.as_view(), name='clear_hand'),
    path('api/entity_image/<str:entity_type>/', EntityImageView.as_view(), name='entity_image'),
]