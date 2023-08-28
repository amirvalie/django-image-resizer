import base64
import binascii
from PIL import Image
from io import BytesIO
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from django.urls import reverse
from .forms import ImageForm, ResizeImageForm
from django.core.exceptions import SuspiciousOperation


class UploadImageView(View):
    forms_class = ImageForm
    def select_target(self):
        targets = {
            reverse('images:image_resize_upload'): reverse('images:image_resize')
        }
        target = targets.get(self.request.path)
        return target if target else reverse('images:image_resize')

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {'form':self.forms_class(),'action':self.select_target()})

    def post(self, request, *args, **kwargs):
        form = self.forms_class(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            image_data = request.FILES.get('image').read()
            encoded_data = base64.b64encode(image_data).decode('utf-8')
            self.request.session['image'] = encoded_data
            return redirect(self.select_target())
        return render(request, 'index.html', {'form':form,'action':self.select_target()})


class ImageResizeView(View):
    resize_image_form = ResizeImageForm
    def get_image(self, delete=False):
        import PIL
        try:
            if delete:
                image_data = self.request.session.pop('image')
            else:
                image_data = self.request.session['image']
        except KeyError:
            raise KeyError('')
        try:
            decoded_data = base64.b64decode(image_data)
            image = Image.open(BytesIO(decoded_data))
        except (binascii.Error, PIL.UnidentifiedImageError):
            raise SuspiciousOperation('')
        return image

    def get(self, request, *args, **kwargs):
        try:
            image = self.get_image()
        except:
            return redirect('images:image_resize_upload')
        image_data = self.request.session.get('image')
        initial_data={
            'width':image.width,
            'height':image.height,
            'format':image.format,
        }
        return render(
            request,
            'image_resizing.html',
            {
                'form':self.resize_image_form(initial=initial_data),
                'image':image_data,
            }
        )

    def post(self, request, *args, **kwargs):
        image = self.get_image(delete=True)
        form = self.resize_image_form(request.POST)
        if form.is_valid():
            return HttpResponse('Ok')
        return render(request, 'image_resizing.html', {'form':form})
