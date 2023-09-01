from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

class ImageResize:
    def __init__(self,
                 image: InMemoryUploadedFile,
                 width: int,
                 height: int,
                 aspect_ratio: bool=True,
                 ) -> None:
        self.image: Image.Image
        self.image = self._open(image)
        self.width = width
        self.height = height
        self.aspect_ratio = aspect_ratio
        self.format= format if format is not None else self.image.format

    def target_file_name(self, image_name: str) -> str:
        file_name = image_name.split('/')[-1].split('.')[0]
        return file_name

    def _open(self, image: InMemoryUploadedFile) -> Image.Image:
        try:
            opened_image = Image.open(image) # type: ignore
            return opened_image # type: ignore
        except IOError:
            raise IOError

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
            f'{self.target_file_name(field.name)}.{self.image.format.lower()}',
            self.resize(),
            save=True,
        )

