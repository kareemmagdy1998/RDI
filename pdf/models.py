from django.db import models

# Create your models here.
class PDFFile(models.Model):
    file = models.FileField(upload_to='uploads/pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    number_of_pages = models.PositiveIntegerField(null=True, blank=True)
    page_width = models.PositiveIntegerField(null=True, blank=True)
    page_height = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"PDF: {self.file.name}"