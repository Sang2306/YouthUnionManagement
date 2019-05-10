"""
    Define some form for website
"""
from django import forms


class UploadFileForm(forms.Form):
    """
        Form upload pdf file
    """
    pdf_file = forms.FileField(label='', widget=forms.FileInput(
        attrs={'accept': 'application/pdf'}))
