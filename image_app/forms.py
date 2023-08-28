from turtle import width
from django import forms
from django.core.exceptions import ValidationError



class ImageForm(forms.Form):
    image = forms.ImageField()

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
    format = forms.ChoiceField(choices=IMAGE_FORMAT_CHOICES)
