from django.db import models

# Create your models here.
class ExtractedText(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    extracted_text = models.TextField()