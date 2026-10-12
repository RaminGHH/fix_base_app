import uuid
import warnings
from io import BytesIO

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

def normalize_avatar(upload):
    """
    Decode and re-encode uploads: do not trust extension or client MIME type
    """
    if upload is None:
        return None
    
    if upload.size > 5 * 1024 * 1024:
        raise ValidationError(
            _("The maximum avatar size is 5 MB")
        )
    
    try:
        upload.seek(0)
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            
            with Image.open(upload) as source:
                if source.format not in {"JPEG", "PNG", "WEBP"}:
                    raise ValidationError(
                        _("Only JPEG, PNG and WebP are accepted")
                    )
                
                if source.width * source.height > 16_000_000:
                    raise ValidationError(
                        _("The maximum image size is 16 million pixels")
                    )
                
                source.seek(0)
                image = ImageOps.exif_transpose(source).convert("RGB")
                image.thumbnail((1024, 1024))
                
                buffer = BytesIO()

                image.save(buffer, format="JPEG", quality=85)

        return ContentFile(
            buffer.getvalue(),
            name=f"{uuid.uuid4().hex}.jpg"    
        )

    except (UnidentifiedImageError, OSError, ValueError, 
            Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValidationError(
            _("The image file is invalid")
        ) from exc
    
    finally:
        upload.seek(0)