from django.db import models

# Create your models here.
class ImageFile(models.Model):
    file = models.ImageField(upload_to='uploads/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    channels = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Image: {self.file.name}"