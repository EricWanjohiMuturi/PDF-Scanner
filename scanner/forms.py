from django import forms

class upload_file(forms.Form):
    file = forms.FileField( widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))
    keyword = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control", "id": "floatingInput", "placeholder": "Enter keyword"}))