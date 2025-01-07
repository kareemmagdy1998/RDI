from rest_framework import serializers
from .models import ImageFile, PDFFile

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'uploaded_at', 'width', 'height', 'channels']
        read_only_fields = ['uploaded_at', 'width', 'height', 'channels']


class PDFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFFile
        fields = ['id', 'file', 'uploaded_at', 'number_of_pages', 'page_width', 'page_height']
        read_only_fields = ['uploaded_at', 'number_of_pages', 'page_width', 'page_height']        