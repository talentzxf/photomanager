from django import forms

from PhotoManager.models import Album


class ScanForm(forms.Form):
    album = forms.ChoiceField(label="Choose an album", widget=forms.Select(), required=True)

    def __init__(self):
        super(ScanForm, self).__init__()
        self.albums = Album.objects.all()
        self.album_list = [(album.name, album.name) for album in self.albums]
        self.fields['album'].choices = self.album_list


class FileUploadForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
