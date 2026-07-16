"""
Image Handler for temporary storage of uploaded images.
Saves base64 images to disk and provides cleanup functionality.
"""
import os
import uuid
import base64
import time
from pathlib import Path
from typing import Tuple, Optional

from utils.wide_event_logger import get_email_logger

# Upload directory path
UPLOAD_DIR = Path(__file__).parent.parent / "assets" / "uploads"

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_mime_extension(mime_type: str) -> str:
    """Get file extension from MIME type."""
    mime_map = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/svg+xml": ".svg",
    }
    return mime_map.get(mime_type.lower(), ".png")


def parse_base64_data(base64_data: str) -> Tuple[bytes, str]:
    """
    Parse base64 data URI and return decoded bytes and MIME type.

    Args:
        base64_data: Data URI string (data:image/png;base64,...)

    Returns:
        Tuple of (decoded_bytes, mime_type)
    """
    if "," in base64_data:
        header, data = base64_data.split(",", 1)
        # Extract MIME type from header like "data:image/png;base64"
        if ":" in header and ";" in header:
            mime_type = header.split(":")[1].split(";")[0]
        else:
            mime_type = "image/png"
    else:
        data = base64_data
        mime_type = "image/png"

    decoded_bytes = base64.b64decode(data)
    return decoded_bytes, mime_type


def save_uploaded_image(base64_data: str, filename: Optional[str] = None) -> str:
    """
    Save a base64-encoded image to disk.

    Args:
        base64_data: Base64-encoded image data (with or without data URI prefix)
        filename: Optional original filename for extension detection

    Returns:
        URL path to the saved image (e.g., "/assets/uploads/uuid.png")
    """
    try:
        # Parse the base64 data
        image_bytes, mime_type = parse_base64_data(base64_data)

        # Determine extension
        if filename:
            ext = Path(filename).suffix.lower()
            if ext not in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
                ext = get_mime_extension(mime_type)
        else:
            ext = get_mime_extension(mime_type)

        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = UPLOAD_DIR / unique_filename

        # Write the file
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # Return the URL path (Dash serves assets automatically)
        return f"/assets/uploads/{unique_filename}"

    except Exception as e:
        print(f"Error saving uploaded image: {e}")
        return ""


def save_multiple_images(base64_images: list, filenames: list = None) -> list:
    """
    Save multiple base64-encoded images to disk.

    Args:
        base64_images: List of base64-encoded image data
        filenames: Optional list of original filenames

    Returns:
        List of URL paths to the saved images
    """
    email_logger = get_email_logger()
    start_time = time.time()

    if not base64_images:
        return []

    if filenames is None:
        filenames = [None] * len(base64_images)

    saved_urls = []
    total_bytes = 0
    image_types = set()

    for img_data, filename in zip(base64_images, filenames):
        if img_data:
            url = save_uploaded_image(img_data, filename)
            if url:
                saved_urls.append(url)
                # Estimate size from base64
                total_bytes += len(img_data) * 3 // 4
                # Extract extension
                if filename:
                    ext = Path(filename).suffix.lower().lstrip(".")
                    if ext:
                        image_types.add(ext)

    duration_ms = (time.time() - start_time) * 1000

    # Log image upload event
    event = email_logger.logger.create_event("storage", "image.uploaded")
    event.set_storage(
        image_count=len(saved_urls),
        total_bytes=total_bytes,
        image_types=list(image_types) if image_types else None,
    )
    event.add_custom("duration_ms", duration_ms)
    event.add_custom("requested_count", len(base64_images))

    if len(saved_urls) == len(base64_images):
        event.success()
    elif len(saved_urls) > 0:
        event.partial(f"Only {len(saved_urls)}/{len(base64_images)} images saved")
    else:
        event.error(error_type="ImageSaveError", error_message="No images were saved")

    event.emit()

    return saved_urls


def cleanup_old_uploads(max_age_hours: int = 24) -> int:
    """
    Remove uploaded files older than max_age_hours.

    Args:
        max_age_hours: Maximum age of files in hours before deletion

    Returns:
        Number of files deleted
    """
    email_logger = get_email_logger()
    start_time = time.time()

    deleted_count = 0
    bytes_freed = 0
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    errors = []

    try:
        for file_path in UPLOAD_DIR.iterdir():
            # Skip .gitkeep and directories
            if file_path.name.startswith(".") or file_path.is_dir():
                continue

            # Check file age
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_count += 1
                    bytes_freed += file_size
                except Exception as e:
                    errors.append(str(e))
                    print(f"Error deleting {file_path}: {e}")

    except Exception as e:
        errors.append(str(e))
        print(f"Error during cleanup: {e}")

    duration_ms = (time.time() - start_time) * 1000

    # Log cleanup event (only if files were processed or errors occurred)
    if deleted_count > 0 or errors:
        event = email_logger.logger.create_event("storage", "image.cleanup")
        event.set_storage(
            files_cleaned=deleted_count,
            bytes_freed=bytes_freed,
        )
        event.add_custom("max_age_hours", max_age_hours)
        event.add_custom("duration_ms", duration_ms)

        if errors:
            event.partial(f"Cleanup completed with {len(errors)} errors")
            event.add_custom("cleanup_errors", errors[:5])  # Limit to 5 errors
        else:
            event.success()

        event.emit()

    return deleted_count


def get_upload_stats() -> dict:
    """
    Get statistics about uploaded files.

    Returns:
        Dict with count, total_size, and oldest_file info
    """
    try:
        files = [f for f in UPLOAD_DIR.iterdir() if not f.name.startswith(".") and f.is_file()]

        if not files:
            return {"count": 0, "total_size_mb": 0, "oldest_hours": 0}

        total_size = sum(f.stat().st_size for f in files)
        oldest_mtime = min(f.stat().st_mtime for f in files)
        oldest_hours = (time.time() - oldest_mtime) / 3600

        return {
            "count": len(files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "oldest_hours": round(oldest_hours, 1),
        }

    except Exception as e:
        print(f"Error getting upload stats: {e}")
        return {"count": 0, "total_size_mb": 0, "oldest_hours": 0}
