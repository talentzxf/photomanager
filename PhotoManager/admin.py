from django.contrib import admin
from django.contrib.admin import helpers
from django.utils.encoding import force_text

from .models import ImageFile, Album


class ImageFileAdmin(admin.ModelAdmin):
    fields = ['local_path', 'modified_time', 'md5', 'file_name','preview_image']
    readonly_fields = ['local_path', 'modified_time', 'md5', 'file_name','preview_image']
    list_display = ['preview_image']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super().changelist_view(request, extra_context)

    def get_changelist(self, request):
        return super().get_changelist(request)


admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(Album)