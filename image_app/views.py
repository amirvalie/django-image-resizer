from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.views import View
from django.urls import reverse
from .forms import ImageForm, ResizeImageForm
from .image_utils.image_resize import ImageResize
from .models import UploadImage
from .tasks import task_image_reize


class UploadImageView(View):
    forms_class = ImageForm

    def select_target(self, **kwargs):
        targets = {
            reverse('images:image_resize_upload'): reverse('images:image_resize', kwargs=kwargs)
        }
        target = targets.get(self.request.path)
        return target if target else reverse('images:image_resize', **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {'form':self.forms_class()})

    def post(self, request, *args, **kwargs):
        form = self.forms_class(request.POST, request.FILES)
        if form.is_valid():
            image_object = form.save()
            print(image_object.image.name)
            uid = urlsafe_base64_encode(force_bytes(image_object.image.name))
            return redirect(self.select_target(uidb64=uid))
        return render(request, 'index.html', {'form':form})


class ImageResizeView(View):
    resize_image_form = ResizeImageForm
    name = None
    def get_object(self):
        image_name = urlsafe_base64_decode(self.kwargs.get('uidb64')).decode()
        return get_object_or_404(UploadImage.objects.all(), image=image_name)

    def get(self, request, *args, **kwargs):
        self.name = 'Amir'
        image_object = self.get_object()
        print('file name in get method:', image_object.image.name)
        initial_data={
            'width':image_object.image.width,
            'height':image_object.image.height,
        }
        return render(
            request,
            'image_resizing.html',
            {
                'form':self.resize_image_form(initial=initial_data),
                'image':image_object.image,
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.resize_image_form(request.POST)
        if form.is_valid():
            image_field = self.get_object().image
            result = task_image_reize.delay(
                image=image_field,
                width=form.cleaned_data['width'],
                height=form.cleaned_data['height'],
                aspect_ratio=form.cleaned_data['aspect_ratio'],
            ) # type: ignore
            uid = result.get()
            return redirect(reverse('images:image_download', kwargs={'uidb64': uid}))
        return render(request, 'image_resizing.html', {'form':form})


class DownloadImageView(View):

    def get_object(self):
        image_name = urlsafe_base64_decode(self.kwargs.get('uidb64')).decode()
        return get_object_or_404(UploadImage.objects.all(), image=image_name)

    def get(self, request, *args, **kwargs):
        return render(request, 'image_download.html', {'image_object':self.get_object()})
