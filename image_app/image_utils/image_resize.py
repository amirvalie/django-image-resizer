from dataclasses import dataclass
from io import BytesIO
from typing import ClassVar, Protocol
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile
from PIL import Image

@dataclass
class BaseImage(Protocol):
    image: Image.Image

    def create_image_file(self) -> ContentFile:
        ...

    def save(self) -> None:
        ...


def open_image(image: ImageFieldFile) -> Image.Image:
    try:
        image = Image.open(image) # type: ignore
        return image # type: ignore
    except IOError:
        raise IOError


def target_file_name(image_name: str) -> str:
    file_name = image_name.split('/')[-1].split('.')[0]
    return file_name

class ImageResize:
    def __init__(self,
                 image: ImageFieldFile,
                 width: int,
                 height: int,
                 aspect_ratio: bool=True,
                 ) -> None:
        self.image = open_image(image)
        self.width = width
        self.height = height
        self.aspect_ratio = aspect_ratio
        self.format= self.image.format

    def resize(self) -> ContentFile:
        if self.aspect_ratio == True:
            self.image.thumbnail((self.width, self.height)) # type: ignore
            return self.create_image_file()
        else:
            img = self.image.resize((self.width, self.height)) # type: ignore
        return self.create_image_file(img)

    def create_image_file(self, img:Image.Image | None=None) -> ContentFile:
        buffer = BytesIO()
        if img:
            img.save(buffer, format=self.format) # type: ignore
        else:
            self.image.save(buffer, format=self.format) # type: ignore
        image_file = ContentFile(buffer.getvalue())
        return image_file

    def save(self, field: ImageFieldFile) -> None:
        field.save(
            f'{target_file_name(field.name)}.{self.image.format.lower()}',
            self.resize(),
            save=True,
        )

