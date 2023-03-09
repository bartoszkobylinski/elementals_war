from django.urls import path
from .views import IndexView, ImageUploadView

app_name = 'elementals_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('upload/', ImageUploadView.as_view(), name='image_upload'),

]