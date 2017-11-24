import uuid

import os
from PIL import Image, ExifTags
from django.utils import timezone

from PhotoManager.models import ImageFile, Album, ImageStatus, ImageMeta
from PhotoManager.settings import DATA_DIR
import face_recognition
import img_rotate


class Utilities:
    _data_dir = DATA_DIR
    img_extension_set = set(['jpg', 'bmp', 'jpeg', 'png'])

    @staticmethod
    def is_image_file_extension(file_extension):
        file_extension = file_extension.lower()
        if file_extension in Utilities.img_extension_set:
            return True
        return False


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
        img_file.album_id = Album.objects.get(name=album).id
        img_file.status = "registered"

        # Access the MD5 field to calculate the MD5 of this file
        img_file.md5

        existing_objs = ImageFile.objects.filter(_md5=img_file.md5)
        if not existing_objs:
            try:
                # Auto rotate the image file
                image, degrees = img_rotate.fix_orientation(full_file_path, save_over=True)
            except:
                pass
            img_file.save()

            # Get meta data from image
            with Image.open(full_file_path) as img:
                if "_getexif" in dir(img) and img._getexif():
                    exif = {
                        ExifTags.TAGS[k]: v
                        for k, v in img._getexif().items()
                        if k in ExifTags.TAGS
                    }
                    img_meta = ImageMeta(img_file, exif, img.format)
                    img_meta.save()
            return True
        return False

    @staticmethod
    def get_face_infor(local_path, file_name):
        full_file_path = os.path.join(local_path, file_name)
        img_to_test = face_recognition.load_image_file(full_file_path)
        face_locations = face_recognition.face_locations(img_to_test)

        found_faces = len(face_locations)
        for face_location in face_locations:
            top, right, bottom, left = face_location
            print("A face is located at pixel Top:{}, Left:{}, Bottom:{}, Right: {}".format(top, left, bottom, right))
            face_image = img_to_test[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            Utilities.save_face_image(pil_image)

        face_encodings = face_recognition.face_encodings(img_to_test, face_locations)
        encoded_faces = len(face_encodings)
        # for face_encoding in face_encodings:
        # print(face_encoding)
        if encoded_faces != found_faces:
            print("ERRORERRORERRORERRORERRORERRORERROR")

    @staticmethod
    def save_face_image(pil_image):
        face_folder = os.path.join(Utilities._data_dir, "faces")
        if not os.path.exists(face_folder):
            os.makedirs(face_folder)
        face_full_path = os.path.join(face_folder, uuid.uuid4().hex + ".jpg")
        pil_image.save(face_full_path, "JPEG")
        return

    @staticmethod
    def scan_data_folder(album):
        scanned_number = 0
        for root, dir, filenames in os.walk(os.path.join(Utilities._data_dir, "raw_images")):
            for filename in filenames:
                if not Utilities.is_image_file_extension(filename.split(".")[-1]):
                    continue
                print("Registering file:{}".format(filename))
                if Utilities.scan_image(root, filename, album):
                    # Utilities.get_face_infor(root, filename)
                    scanned_number += 1
                print("Scanning file:{}".format(filename))
                print("File:{} done".format(filename))
        print("All Done!")
        return scanned_number

    @staticmethod
    def upload_file(file):
        with open(os.path.join(Utilities._data_dir, "raw_images", file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            Utilities.scan_image(Utilities._data_dir, file.name)
            # Utilities.get_face_infor(Utilities._data_dir, file.name)
        return True
