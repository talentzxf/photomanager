import os

from PIL import Image
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from PhotoManager.Forms import ScanForm, FileUploadForm
from PhotoManager.models import ImageFile, Album
from PhotoManager.utilities import Utilities


class ResultsView(generic.ListView):
    template_name = "photomanager/index.html"
    context_object_name = 'img_list'

    def get_queryset(self):
        return ImageFile.objects.order_by('-modified_time')

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['form'] = ScanForm()
        context['upload_form'] = FileUploadForm()
        return context


def scan(request):
    if request.method != 'POST':
        return HttpResponse(status=409, content="Not Allowed!")
    album = request.POST.get('album')
    total_uploaded = Utilities.scan_data_folder(album)
    return HttpResponse("Totally uploaded:%d files!" % total_uploaded)


def upload(request):
    if request.method == 'POST':
        fileUploadForm = FileUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        file_count = 0
        for f in files:
            if Utilities.upload_file(f):
                file_count += 1
        return HttpResponse("Totally uploaded:%d files" % file_count)
    else:
        return HttpResponse(status=409, content="Not Allowed!")


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
