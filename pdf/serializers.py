from rest_framework import serializers
from .models import PDFFile

class PDFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFFile
        fields = ['id', 'file', 'uploaded_at', 'number_of_pages', 'page_width', 'page_height']
        read_only_fields = ['uploaded_at', 'number_of_pages', 'page_width', 'page_height']