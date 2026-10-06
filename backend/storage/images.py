import io
from dataclasses import dataclass

from PIL import Image, ImageOps, UnidentifiedImageError

from backend.config import settings

# Accepted upload formats, keyed by the format name Pillow reports.
ALLOWED_FORMATS: dict[str, tuple[str, str]] = {
    # PIL format: (content type, file extension)
    "JPEG": ("image/jpeg", "jpg"),
    "PNG": ("image/png", "png"),
    "WEBP": ("image/webp", "webp"),
}

# Thumbnails are always JPEG: smallest payload with universal browser support.
THUMBNAIL_CONTENT_TYPE = "image/jpeg"
THUMBNAIL_EXTENSION = "jpg"

# Decompression-bomb guards, checked against the header before any pixel is
# decoded: a 100 KB file can otherwise expand into gigabytes of bitmap.
MAX_SIDE_PX = 10_000
MAX_PIXELS = 50_000_000


class InvalidImageError(ValueError):
    """The uploaded bytes are not a usable image."""


class UnsupportedImageFormatError(ValueError):
    """The image decoded fine but its format is not one we accept."""


@dataclass(frozen=True)
class ProcessedImage:
    """A normalized upload: re-encoded original plus a generated thumbnail."""

    data: bytes
    content_type: str
    extension: str
    width: int
    height: int
    thumbnail: bytes


def _flatten(image: Image.Image) -> Image.Image:
    """Composite transparency onto white so the JPEG thumbnail is not blotchy."""
    if image.mode in ("RGBA", "LA", "P"):
        rgba = image.convert("RGBA")
        canvas = Image.new("RGB", rgba.size, (255, 255, 255))
        canvas.paste(rgba, mask=rgba.split()[-1])
        return canvas
    return image.convert("RGB")


def _encode(image: Image.Image, pil_format: str) -> bytes:
    buffer = io.BytesIO()
    if pil_format == "JPEG":
        _flatten(image).save(buffer, "JPEG", quality=90, optimize=True, progressive=True)
    elif pil_format == "PNG":
        image.save(buffer, "PNG", optimize=True)
    else:  # WEBP
        image.save(buffer, "WEBP", quality=90, method=4)
    return buffer.getvalue()


def _thumbnail(image: Image.Image) -> bytes:
    thumb = _flatten(image.copy())
    # thumbnail() keeps the aspect ratio and never upscales.
    thumb.thumbnail((settings.MEDIA_THUMBNAIL_MAX_PX, settings.MEDIA_THUMBNAIL_MAX_PX))
    buffer = io.BytesIO()
    thumb.save(buffer, "JPEG", quality=80, optimize=True, progressive=True)
    return buffer.getvalue()


def process(raw: bytes) -> ProcessedImage:
    """Validate, normalize and derive a thumbnail from uploaded image bytes.

    The original is re-encoded rather than stored verbatim: that applies the EXIF
    orientation (so portrait photos are not served sideways) and drops the rest of
    the EXIF block, GPS coordinates included.
    """
    if not raw:
        raise InvalidImageError("Uploaded file is empty")

    try:
        image = Image.open(io.BytesIO(raw))
    except UnidentifiedImageError as exc:
        raise InvalidImageError("Uploaded file is not a readable image") from exc
    except Image.DecompressionBombError as exc:
        raise InvalidImageError("Image is too large to decode") from exc
    except OSError as exc:
        raise InvalidImageError(f"Image could not be decoded: {exc}") from exc

    pil_format = image.format or ""
    if pil_format not in ALLOWED_FORMATS:
        supported = ", ".join(sorted(ALLOWED_FORMATS))
        raise UnsupportedImageFormatError(
            f"Unsupported image format {pil_format or 'unknown'} (supported: {supported})"
        )

    # Header-only checks: image.size is known before the pixels are loaded.
    width, height = image.size
    if width < 1 or height < 1:
        raise InvalidImageError("Image has no pixels")
    if max(width, height) > MAX_SIDE_PX or width * height > MAX_PIXELS:
        raise InvalidImageError(
            f"Image is too large ({width}x{height}); "
            f"max {MAX_SIDE_PX}px per side and {MAX_PIXELS} pixels total"
        )

    content_type, extension = ALLOWED_FORMATS[pil_format]

    try:
        oriented = ImageOps.exif_transpose(image) or image
        # exif_transpose may swap the axes, so read the size back off the result.
        width, height = oriented.size
        return ProcessedImage(
            data=_encode(oriented, pil_format),
            content_type=content_type,
            extension=extension,
            width=width,
            height=height,
            thumbnail=_thumbnail(oriented),
        )
    except OSError as exc:  # truncated/corrupt pixel data surfaces here
        raise InvalidImageError(f"Image could not be processed: {exc}") from exc
