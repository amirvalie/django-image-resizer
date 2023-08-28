from django.urls import path
from .views import ImageResizeView, UploadImageView

app_name = 'images'

urlpatterns = [
    path('', UploadImageView.as_view(), name='image_resize_upload'),
    path('reformat-image/', UploadImageView.as_view(), name='image_reformat'),
    path('compressor-image/', UploadImageView.as_view(), name='image_compressor'),
    path('crop-image/', UploadImageView.as_view(), name='image_crop'),
    path('rotate-image/', UploadImageView.as_view(), name='image_rotate'),
    path('resize-image/', ImageResizeView.as_view(), name='image_resize')
]






