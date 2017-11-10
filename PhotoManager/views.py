from PIL import Image
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from PhotoManager.models import ImageFile


class ResultsView(generic.ListView):
    template_name = "photomanager/index.html"
    context_object_name = 'img_list'

    def get_queryset(selfself):
        return ImageFile.objects.order_by('-modified_time')[:5]


def img(request, img_id):
    try:
        img_desc = get_object_or_404(ImageFile, pk=img_id)
    except ImageFile.DoesNotExist:
        raise Http404("Image not found!")

    img_full_path = img_desc.local_path + "\\" + img_desc.file_name
    try:
        with open(img_full_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
