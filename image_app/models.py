from django.db import models

# Create your models here.


class UploadImage(models.Model):
    image = models.ImageField(upload_to='image')

    def __str__(self) -> str:
        return self.image.name