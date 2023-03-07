from django.urls import path
from .views import IndexView, GameView, ImageUploadView, ElementImageUploadView

app_name = 'elementals_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('game/', GameView.as_view(), name='game'),
    path('upload/wizard/', ImageUploadView.as_view(), name='upload_wizard'),
    path('upload/element/', ElementImageUploadView.as_view(), name='upload_element'),
    path('upload/', ImageUploadView.as_view(), name='image_upload'),

]