from datetime import datetime
import inspect
from enum import Enum

import os
from PIL import ExifTags

from django.db import models
from django.utils.safestring import mark_safe
import hashlib


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not (m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class ImageStatus(ChoiceEnum):
    unknown = 0
    registered = 1
    scanned = 2
    face_recognition_done = 3


class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return "%s" % self.name


class ImageFile(models.Model):
    local_path = models.CharField(max_length=500)
    _md5 = models.CharField(max_length=33, blank=True, db_column='md5', db_index=True)
    modified_time = models.DateTimeField('Date Modified')
    file_name = models.CharField(max_length=200)
    album_id = models.IntegerField(db_index=True)
    status = models.CharField(max_length=10, choices=ImageStatus.choices(), default="registered")

    def __str__(self):
        return "%d_%s" % (self.id, self.file_name)

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


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info_raw = exif_data["GPSInfo"]
        gps_info = {}
        for key in gps_info_raw.keys():
            decode = ExifTags.GPSTAGS.get(key, key)
            gps_info[decode] = gps_info_raw[key]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon


class ImageMeta(models.Model):
    image_id = models.IntegerField(db_index=True)
    image_creation_time = models.DateTimeField(blank=True, null=True)
    image_longitude = models.DecimalField(decimal_places=10, max_digits=15, blank=True, null=True)
    image_latitude = models.DecimalField(decimal_places=10, max_digits=15, blank=True, null=True)
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    img_format = models.CharField(max_length=5)

    def __init__(self, image_file, exif, type):
        super(ImageMeta, self).__init__()
        self.image_id = image_file.id
        if 'DateTime' in exif:
            self.image_creation_time = datetime.strptime(exif['DateTime'], "%Y:%m:%d %H:%M:%S")
        self.image_latitude, self.image_longitude = get_lat_lon(exif)
        self.image_width = exif["ExifImageWidth"]
        self.image_height = exif["ExifImageHeight"]
        self.image_format = type
