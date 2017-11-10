import os

from django.db import models
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
import hashlib


class Album(models.Model):
    name = models.CharField(max_length=50,primary_key=True)

    def __str__(self):
        return "%s" % self.name


class ImageFile(models.Model):
    local_path = models.CharField(max_length=500)
    _md5 = models.CharField(max_length=33, blank=True, db_column='md5', db_index=True)
    modified_time = models.DateTimeField('Date Modified')
    file_name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name

    def preview_image(self):
        return mark_safe(u'<img src="/img/%s" width="160px" height="120px" title="%s" />' % (self.id, self.file_name))

    preview_image.short_description = 'Pre-view Image'

    @property
    def md5(self):
        # Nothing was set, may be used in some weird places
        if not self.id and not self.file_name and not self.local_path:
            return ''

        if not self._md5:
            img_path = os.path.join(self.local_path, self.file_name)
            self._md5 = hashlib.md5(open(img_path, 'rb').read()).hexdigest()
        return self._md5

    @md5.setter
    def md5(self, value):
        self._md5 = value
