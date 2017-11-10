from django import forms

from PhotoManager.models import Album


class ScanForm(forms.Form):
    folder_path = forms.CharField(label="Please input server path here", max_length=100)
    albums = Album.objects.all()
    album_list = [(album.name, album.name) for album in albums]
    album = forms.ChoiceField(label="Choose an album", choices=album_list, widget=forms.Select(), required=True)
