from PIL import UnidentifiedImageError, Image
from django.forms import ValidationError
import magic


def validate_file_content(file, expected_mime_types):
        """
        Validate file MIME type using magic library.
        """
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(file.read(2048))
        file.seek(0)  # Reset file pointer after reading
        if mime_type not in expected_mime_types:
            raise ValidationError(f"Invalid file type: {mime_type}. Expected one of {expected_mime_types}.")
        return mime_type


def validate_image(file):
        """
        Validate image content and extract metadata.
        """
        try:
            img = Image.open(file)
            img.verify()  # Ensure it's a valid image file
            file.seek(0)  # Reset file pointer after verification
            return img
        except UnidentifiedImageError:
            raise ValidationError("Invalid image file.")    