import base64
from io import BytesIO
from PIL import UnidentifiedImageError, Image
from django.forms import ValidationError
import magic
from django.core.files.uploadedfile import InMemoryUploadedFile


def decode_base64_file(base64_string, expected_mime_types):
    """
    Decodes a Base64-encoded file and validates its MIME type.

    :param base64_string: The Base64-encoded file string
    :param expected_mime_types: List of allowed MIME types
    :return: A Django InMemoryUploadedFile object and its MIME type
    """
    try:
        # Extract the Base64 header and data
        header, base64_data = base64_string.split(";base64,")
        file_name = header.split("/")[-1]  # Extract file extension from MIME type
        decoded_file = BytesIO(base64.b64decode(base64_data))

        # Validate MIME type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(decoded_file.read(2048))
        decoded_file.seek(0)  # Reset file pointer after reading
        if mime_type not in expected_mime_types:
            raise ValidationError(f"Invalid file type: {mime_type}. Expected one of {expected_mime_types}.")

        # Wrap the BytesIO object in an InMemoryUploadedFile
        in_memory_file = InMemoryUploadedFile(
            file=decoded_file,
            field_name=None,
            name=f"uploaded_file.{file_name.split('/')[-1]}",
            content_type=mime_type,
            size=len(decoded_file.getvalue()),
            charset=None,
        )
        return in_memory_file, mime_type

    except (ValueError, IndexError, base64.binascii.Error) as e:
        raise ValidationError(f"Invalid Base64 format: {e}")


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