from rest_framework import serializers
from .models import ImageFile

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'uploaded_at', 'width', 'height', 'channels']
        read_only_fields = ['uploaded_at', 'width', 'height', 'channels']