import magic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import ImageFile
from pdf.models import PDFFile 
from .serializers import ImageFileSerializer
from pdf.serializers import PDFFileSerializer
from .utils import validate_file_content , validate_image
from pdf.utils import validate_pdf


class FileUploadView(APIView):
    """
    Endpoint: POST /api/upload/
    Accepts image and PDF files, validates their content, saves them, and returns metadata.
    """

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validate file content
            mime_type = validate_file_content(file, expected_mime_types=["image/jpeg", "image/png", "application/pdf"])

            if mime_type.startswith("image/"):
                # Process and save image
                img = validate_image(file)
                image_file = ImageFile.objects.create(
                    file=file,
                    width=img.width,
                    channels=len(img.getbands())
                )
                serializer = ImageFileSerializer(image_file)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif mime_type == "application/pdf":
                # Process and save PDF
                pdf_reader = validate_pdf(file)
                page = pdf_reader.pages[0]
                pdf_file = PDFFile.objects.create(
                    file=file,
                    number_of_pages=len(pdf_reader.pages),
                    page_width=int(page.mediabox.width),
                    page_height=int(page.mediabox.height)
                )
                serializer = PDFFileSerializer(pdf_file)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)
