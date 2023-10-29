from django import forms
from .models import ExtractedText

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = ExtractedText
        fields = ['pdf_file']