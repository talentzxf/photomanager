import os
from django.utils import timezone

from PhotoManager.models import ImageFile, Album
from PhotoManager.settings import DATA_DIR


class Utilities:
    _data_dir = DATA_DIR

    @staticmethod
    def scan_image(local_path, file_name, album='DEFAULT_ALBUM'):
        '''
        :param file_name:
        :param album:
        :return: True -- The file is successfully saved  False -- The file existed before.
        '''
        full_file_path = os.path.join(local_path, file_name)
        img_file = ImageFile()
        img_file.local_path = local_path
        img_file.file_name = file_name
        img_file.modified_time = timezone.now()
        img_file.album = Album.objects.get(name=album)
        # Access the MD5 field to calculate the MD5 of this file
        img_file.md5

        existing_objs = ImageFile.objects.filter(_md5=img_file.md5)
        if not existing_objs:
            img_file.save()
            return True
        return False

    @staticmethod
    def scan_data_folder(album):
        scanned_number = 0
        for root, dir, files in os.walk(Utilities._data_dir):
            for file in files:
                if Utilities.scan_image(root, file, album):
                    scanned_number += 1
        return scanned_number

    @staticmethod
    def upload_file(file):
        with open(os.path.join(Utilities._data_dir, file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            Utilities.scan_image(Utilities._data_dir, file.name)
        return True
