from django.db import models


class ImageFile(models.Model):
    local_path = models.CharField(max_length=500)
    md5 = models.CharField(max_length=33, blank=True)
    modified_time = models.DateTimeField('Date Modified')
    file_name = models.CharField(max_length=200)

    def __str__(self):
        return self.file_name
