from django.db import models
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class ImageFile(models.Model):
    local_path = models.CharField(max_length=500)
    md5 = models.CharField(max_length=33, blank=True)
    modified_time = models.DateTimeField('Date Modified')
    file_name = models.CharField(max_length=200)

    def __str__(self):
        return self.file_name

    def preview_image(self):
        return mark_safe(u'<img src="/img/%s" width="160px" height="120px" />' % self.id)

    preview_image.short_description = 'Pre-view Image'
