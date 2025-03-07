from django import forms


class UploadFileForm(forms.Form):
    upl_file = forms.FileField(label='File', widget=forms.FileInput(attrs={'class':'form-control'}))
    