from celery import shared_task
from .image_utils.image_resize import ImageResize
from django.db.models.fields.files import ImageFieldFile
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes



@shared_task(serializer='pickle')
def task_image_reize(image: ImageFieldFile,
        width: int, height:int,
        aspect_ratio: bool,):
    image_resize = ImageResize(
        image=image,
        width=width,
        height=height,
        aspect_ratio=aspect_ratio,
    )
    image_resize.save(field = image)
    uid = urlsafe_base64_encode(force_bytes(image.name))
    return uid
