from django.shortcuts import get_object_or_404
import magic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import ImageFile,PDFFile 
from .serializers import ImageFileSerializer,PDFFileSerializer
from .utils import decode_base64_file , validate_image , validate_pdf


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