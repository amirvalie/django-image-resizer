from django.urls import path
from .views import ImageResizeView, UploadImageView, DownloadImageView

app_name = 'images'

urlpatterns = [
    path('', UploadImageView.as_view(), name='image_resize_upload'),
    path('resize-image/<uidb64>/', ImageResizeView.as_view(), name='image_resize'),
    path('download/<uidb64>/', DownloadImageView.as_view(), name='image_download'),
]






