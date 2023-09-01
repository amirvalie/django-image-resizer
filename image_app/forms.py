from turtle import width
from django import forms
from django.core.exceptions import ValidationError
from traitlets import default
from .models import UploadImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ('image',)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        megabyte_limit = 10
        if image.size > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        return image


IMAGE_FORMAT_CHOICES = (
    ('jpg', 'JPG'),
    ('png', 'PNG'),
    ('webp', 'WEBP'),
)

class ResizeImageForm(forms.Form):
    width = forms.IntegerField(max_value=2000)
    height = forms.IntegerField(max_value=2000)
    aspect_ratio = forms.BooleanField(
        label='Preserve Aspect Ratio',
        help_text='Select whether to preserve the aspect ratio of the image.',
        initial=True,
        required=False,
    )