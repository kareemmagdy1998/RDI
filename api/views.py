from django.shortcuts import get_object_or_404
import magic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import ImageFile,PDFFile 
from .serializers import ImageFileSerializer,PDFFileSerializer
from .utils import decode_base64_file , validate_image , validate_pdf
import os
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


class FileUploadView(APIView):
    """
    Endpoint: POST /api/upload/
    Accepts image and PDF files, validates their content, saves them, and returns metadata.
    """

    def post(self, request):
        file = request.data.get('file')
        file_name = request.data.get('file_name')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validate file content
            decoded_file,mime_type = decode_base64_file(file,file_name,expected_mime_types=["image/jpeg", "image/png", "application/pdf"])

            if mime_type.startswith("image/"):
                # Process and save image
                img = validate_image(decoded_file)
                image_file = ImageFile.objects.create(
                    file=decoded_file,
                    width=img.width,
                    height=img.height,
                    channels=len(img.getbands())
                )
                serializer = ImageFileSerializer(image_file)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif mime_type == "application/pdf":
                # Process and save PDF
                pdf_reader = validate_pdf(decoded_file)
                page = pdf_reader.pages[0]
                pdf_file = PDFFile.objects.create(
                    file=decoded_file,
                    number_of_pages=len(pdf_reader.pages),
                    page_width=int(page.mediabox.width),
                    page_height=int(page.mediabox.height)
                )
                serializer = PDFFileSerializer(pdf_file)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)


class ImageListView(APIView):
    """
    Endpoint: GET /api/images/
    Returns a list of all uploaded images.
    """
    def get(self, request):
        images = ImageFile.objects.all()
        serializer = ImageFileSerializer(images, many=True)
        return Response(serializer.data)


class PDFListView(APIView):
    """
    Endpoint: GET /api/pdfs/
    Returns a list of all uploaded PDFs.
    """
    def get(self, request):
        pdfs = PDFFile.objects.all()
        serializer = PDFFileSerializer(pdfs, many=True)
        return Response(serializer.data)


class ImageDetailView(APIView):
    """
    Endpoint: GET /api/images/{id}/
    Returns metadata of a specific image.
    """
    def get(self, request, id):
        image = get_object_or_404(ImageFile, id=id)
        serializer = ImageFileSerializer(image)
        return Response(serializer.data)


class PDFDetailView(APIView):
    """
    Endpoint: GET /api/pdfs/{id}/
    Returns metadata of a specific PDF.
    """
    def get(self, request, id):
        pdf = get_object_or_404(PDFFile, id=id)
        serializer = PDFFileSerializer(pdf)
        return Response(serializer.data)

class ImageDeleteView(APIView):
    """
    Endpoint: DELETE /api/images/{id}/
    Deletes a specific image.
    """
    def delete(self, request, id):
        image = get_object_or_404(ImageFile, id=id)
        image.file.delete(save=False)  # Deletes the file from storage
        image.delete()  # Deletes the record from the database
        return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)    

class PDFDeleteView(APIView):
    """
    Endpoint: DELETE /api/pdfs/{id}/
    Deletes a specific PDF.
    """
    def delete(self, request, id):
        pdf = get_object_or_404(PDFFile, id=id)
        pdf.file.delete(save=False)  # Deletes the file from storage
        pdf.delete()  # Deletes the record from the database
        return Response({"message": "PDF deleted successfully"}, status=status.HTTP_204_NO_CONTENT)    


class RotateImageView(APIView):
    """
    Endpoint: POST /api/rotate/
    Rotates an image by a specified angle.
    """
    def post(self, request):
        image_id = request.data.get("image_id")
        angle = request.data.get("angle")

        if not image_id or not angle:
            return Response({"error": "Image ID and angle are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = get_object_or_404(ImageFile, id=image_id)
            img_path = image.file.path

            # Open and rotate the image
            with Image.open(img_path) as img:
                rotated_image = img.rotate(int(angle), expand=True)
                rotated_image_io = BytesIO()
                rotated_image.save(rotated_image_io, format=img.format)

            # Save rotated image back to file system
            rotated_filename = f"rotated_{os.path.basename(img_path)}"
            rotated_file = ContentFile(rotated_image_io.getvalue())
            image.file.save(rotated_filename, rotated_file)

            # Update metadata in the database
            rotated_image = Image.open(image.file.path)
            image.width, image.height = rotated_image.size
            image.save()

            serializer = ImageFileSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    