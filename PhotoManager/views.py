from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render

from PhotoManager.models import ImageFile


def index(request):
    img_list = ImageFile.objects.order_by('-modified_time')[:5]
    context = {
        'img_list': img_list,
    }
    return render(request, "photomanager/index.html", context)


def img(request, img_id):
    img_desc = ImageFile.objects.get(pk=img_id)
    img_full_path = img_desc.local_path + "\\" + img_desc.file_name
    try:
        with open(img_full_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
