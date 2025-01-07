
from PyPDF2 import PdfReader
from django.forms import ValidationError


def validate_pdf(file):
        """
        Validate PDF content and extract metadata.
        """
        try:
            pdf_reader = PdfReader(file)
            if not pdf_reader.pages:
                raise ValidationError("The PDF file is empty or invalid.")
            return pdf_reader
        except Exception as e:
            raise ValidationError(f"Invalid PDF file: {e}")