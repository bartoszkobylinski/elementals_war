from django.urls import path
from .views import IndexView, GameView, UploadWizardImage

app_name = 'elementals_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('game/', GameView.as_view(), name='game'),
    path('upload_wizard_image/', UploadWizardImage.as_view(), name='upload_wizard_image'),
]