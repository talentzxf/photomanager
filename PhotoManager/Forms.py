from django import forms

from PhotoManager.models import Album


class ScanForm(forms.Form):
    def __init__(self):
        self.folder_path = forms.CharField(label="Please input server path here", max_length=100)
        self.albums = Album.objects.all()
        self.album_list = [(album.name, album.name) for album in albums]
        self.album = forms.ChoiceField(label="Choose an album", choices=album_list, widget=forms.Select(),
                                       required=True)
