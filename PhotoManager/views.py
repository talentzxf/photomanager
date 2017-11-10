import os

from PIL import Image
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from PhotoManager.Forms import ScanForm
from PhotoManager.models import ImageFile, Album


class ResultsView(generic.ListView):
    template_name = "photomanager/index.html"
    context_object_name = 'img_list'

    def get_queryset(self):
        return ImageFile.objects.order_by('-modified_time')[:5]

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['form'] = ScanForm()
        return context


def scan(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed("Bad request")
    local_path = request.POST.get("folder_path")
    if not os.path.isdir(local_path):
        raise Http404("Folder not exist")

    album = request.POST.get('album')
    total_uploaded = 0
    total_modified = 0
    for root, dir, files in os.walk(local_path):
        for file in files:
            full_file_path = os.path.join(root, file)
            imgFile = ImageFile()
            imgFile.local_path = root
            imgFile.file_name = file
            imgFile.modified_time = timezone.now()
            imgFile.album = Album.objects.get(name=album)
            imgFile.md5

            existing_objs = ImageFile.objects.filter(_md5=imgFile.md5)
            if not existing_objs:
                imgFile.save()
                total_uploaded = total_uploaded + 1
            else:
                existing_obj = existing_objs[0]
                existing_obj.modified_time = imgFile.modified_time
                existing_obj.save()
                total_modified = total_modified + 1
    return HttpResponse("Totally uploaded:%d files, totally modified:%d files" % (total_uploaded, total_modified))


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
