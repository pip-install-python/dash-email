"""
Email Sender using Resend API.
Includes HTML generation from dash_email components.
Supports inline image embedding using CID (Content-ID).
"""
import os
import re
import time
import base64
import uuid
import mimetypes
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv
import resend

from utils.wide_event_logger import get_email_logger

# Load environment variables
load_dotenv()

# Initialize Resend with API key
resend.api_key = os.getenv("RESEND_API_KEY")

# Base path for assets
ASSETS_DIR = Path(__file__).parent.parent / "assets"


def get_mime_type(filename: str) -> str:
    """Get MIME type from filename."""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def extract_local_images(html: str) -> List[str]:
    """
    Extract all local image URLs from HTML.

    Args:
        html: HTML string to parse

    Returns:
        List of local image URLs (e.g., ['/assets/uploads/abc.png'])
    """
    # Match src="/assets/..." or src='/assets/...'
    pattern = r'src=["\'](/assets/[^"\']+)["\']'
    matches = re.findall(pattern, html)
    return list(set(matches))  # Remove duplicates


def create_inline_attachments(image_urls: List[str]) -> Tuple[List[Dict], Dict[str, str]]:
    """
    Create inline attachments for Resend API from local image URLs.

    Args:
        image_urls: List of local image URLs (e.g., ['/assets/uploads/abc.png'])

    Returns:
        Tuple of (attachments list, url_to_cid mapping)
    """
    attachments = []
    url_to_cid = {}

    for url in image_urls:
        # Convert URL path to file path
        # /assets/uploads/abc.png -> assets/uploads/abc.png
        relative_path = url.lstrip('/')
        file_path = Path(__file__).parent.parent / relative_path

        if not file_path.exists():
            print(f"Warning: Image file not found: {file_path}")
            continue

        try:
            # Read file and encode as base64
            with open(file_path, 'rb') as f:
                content = f.read()

            # Generate unique content ID
            content_id = f"img-{uuid.uuid4().hex[:8]}"

            # Get filename and mime type
            filename = file_path.name
            content_type = get_mime_type(filename)

            # Create attachment dict for Resend
            # Two options for inline images:

            # OPTION 1: Base64 encoded string (testing this approach)
            # Send the image content directly as a base64 string
            # Docs recommend adding content_type for better client rendering
            attachment = {
                "content": base64.b64encode(content).decode('utf-8'),
                "filename": filename,
                "content_id": content_id,
                "content_type": content_type,
            }

            # OPTION 2: List of bytes (Python SDK native approach)
            # Per Resend Python docs: {"content": list(f), "filename": "...", "content_id": "..."}
            # attachment = {
            #     "content": list(content),
            #     "filename": filename,
            #     "content_id": content_id,
            #     "content_type": content_type,
            # }

            attachments.append(attachment)
            url_to_cid[url] = content_id

        except Exception as e:
            print(f"Error processing image {url}: {e}")
            continue

    return attachments, url_to_cid


def replace_urls_with_cid(html: str, url_to_cid: Dict[str, str]) -> str:
    """
    Replace local image URLs with CID references in HTML.

    Args:
        html: Original HTML string
        url_to_cid: Mapping of URL to content ID

    Returns:
        HTML with cid: references instead of local URLs
    """
    for url, cid in url_to_cid.items():
        # Replace src="/assets/..." with src="cid:content-id"
        html = html.replace(f'src="{url}"', f'src="cid:{cid}"')
        html = html.replace(f"src='{url}'", f"src='cid:{cid}'")

    return html


def prepare_email_with_images(html: str) -> Tuple[str, List[Dict]]:
    """
    Prepare HTML email with inline image attachments.

    Args:
        html: Original HTML with local image URLs

    Returns:
        Tuple of (modified HTML with CID references, attachments list)
    """
    # Extract local images
    image_urls = extract_local_images(html)

    if not image_urls:
        return html, []

    # Create attachments and get CID mapping
    attachments, url_to_cid = create_inline_attachments(image_urls)

    # Replace URLs with CID references
    modified_html = replace_urls_with_cid(html, url_to_cid)

    return modified_html, attachments


def create_file_attachments(file_data: List[Dict]) -> List[Dict]:
    """
    Create file attachments for Resend API.

    Args:
        file_data: List of {"content": base64_string, "filename": "doc.pdf"}

    Returns:
        List of attachment dicts for Resend
    """
    attachments = []
    for file in file_data:
        content = file.get("content", "")
        filename = file.get("filename", "attachment")

        # If content has data URI prefix, strip it
        if "," in content and content.startswith("data:"):
            content = content.split(",", 1)[1]

        attachment = {
            "content": content,  # Already base64
            "filename": filename,
        }

        # Add content_type if detectable
        content_type = get_mime_type(filename)
        if content_type:
            attachment["content_type"] = content_type

        attachments.append(attachment)

    return attachments


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    from_email: str = "onboarding@resend.dev",
    embed_images: bool = True,
    scheduled_at: Optional[str] = None,
    file_attachments: Optional[List[Dict]] = None,
) -> dict:
    """
    Send an email using Resend API with inline image support.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        html_content: HTML content of the email
        from_email: Sender email address (default: Resend test email)
        embed_images: Whether to embed local images as inline attachments (default: True)
        scheduled_at: Optional schedule time (ISO 8601 or natural language like "in 1 hour")
        file_attachments: Optional list of file attachments [{"content": base64, "filename": "doc.pdf"}]

    Returns:
        dict with 'success' boolean and 'message' or 'error'
    """
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        # Prepare all attachments
        all_attachments = []

        # 1. Inline images (existing logic)
        if embed_images:
            html_content, image_attachments = prepare_email_with_images(html_content)
            all_attachments.extend(image_attachments)

        # 2. File attachments (new)
        if file_attachments:
            file_atts = create_file_attachments(file_attachments)
            all_attachments.extend(file_atts)

        params = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }

        # Add attachments if any
        if all_attachments:
            params["attachments"] = all_attachments

        # Add scheduled_at if provided (max 30 days in advance)
        if scheduled_at:
            params["scheduled_at"] = scheduled_at

        response = resend.Emails.send(params)
        duration_ms = (time.time() - start_time) * 1000

        # Count attachments by type
        inline_count = len(image_attachments) if embed_images else 0
        file_count = len(file_atts) if file_attachments else 0

        # Log successful email send
        event = email_logger.logger.create_event("email", "email.sent")
        event.set_email(
            recipient=to_email,
            subject=subject,
            from_addr=from_email,
            html_size_bytes=len(html_content),
            image_count=inline_count,
        )
        event.add_custom("send_provider", "resend")
        event.add_custom("email_id", response.get("id", "N/A"))
        event.add_custom("duration_ms", duration_ms)
        event.add_custom("inline_images", inline_count)
        event.add_custom("file_attachments", file_count)
        event.add_custom("total_attachments", len(all_attachments))
        event.add_custom("scheduled", scheduled_at is not None)
        if scheduled_at:
            event.add_custom("scheduled_at", scheduled_at)
        event.success()
        event.emit()

        # Build success message
        message = f"Email sent successfully! ID: {response.get('id', 'N/A')}"
        if scheduled_at:
            message = f"Email scheduled! ID: {response.get('id', 'N/A')}"

        return {
            "success": True,
            "message": message,
            "response": response,
            "inline_images": inline_count,
            "file_attachments": file_count,
            "scheduled": scheduled_at is not None,
        }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Log failed email send
        event = email_logger.logger.create_event("email", "email.sent")
        event.set_email(
            recipient=to_email,
            subject=subject,
            from_addr=from_email,
            html_size_bytes=len(html_content),
        )
        event.add_custom("send_provider", "resend")
        event.add_custom("duration_ms", duration_ms)
        event.add_custom("attachments_attempted", len(all_attachments) if 'all_attachments' in dir() else 0)
        event.add_custom("scheduled_attempted", scheduled_at is not None)
        event.error(exception=e)
        event.emit()

        return {
            "success": False,
            "error": str(e),
        }


def send_batch_emails(
    recipients: List[str],
    subject: str,
    html_content: str,
    from_email: str = "onboarding@resend.dev",
    template_id: Optional[str] = None,
    template_data_list: Optional[List[Dict]] = None,
) -> dict:
    """
    Send batch emails via Resend Batch API.

    Note: Batch endpoint does NOT support attachments or scheduling.

    Args:
        recipients: List of recipient email addresses (max 100)
        subject: Email subject line
        html_content: HTML content of the email (ignored if template_id provided)
        from_email: Sender email address
        template_id: Optional Resend template ID
        template_data_list: Optional list of template variable dicts per recipient

    Returns:
        dict with success status, counts, and response data
    """
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        # Enforce Resend's 100 email limit
        recipients = recipients[:100]

        # Build batch params
        batch_params = []

        for i, recipient in enumerate(recipients):
            email_params = {
                "from": from_email,
                "to": [recipient],
                "subject": subject,
            }

            if template_id:
                email_params["template_id"] = template_id
                if template_data_list and i < len(template_data_list):
                    email_params["template_data"] = template_data_list[i]
            else:
                email_params["html"] = html_content

            batch_params.append(email_params)

        # Send batch
        result = resend.Batch.send(batch_params)
        duration_ms = (time.time() - start_time) * 1000

        # Log successful batch send
        event = email_logger.logger.create_event("email", "email.batch_sent")
        event.set_email(
            subject=subject,
            from_addr=from_email,
        )
        event.add_custom("send_provider", "resend")
        event.add_custom("batch_size", len(recipients))
        event.add_custom("duration_ms", duration_ms)
        event.add_custom("used_template", template_id is not None)
        if template_id:
            event.add_custom("template_id", template_id)
        event.success()
        event.emit()

        return {
            "success": True,
            "message": f"Batch sent successfully! {len(recipients)} emails queued.",
            "total": len(recipients),
            "data": result,
        }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Log failed batch send
        event = email_logger.logger.create_event("email", "email.batch_sent")
        event.set_email(
            subject=subject,
            from_addr=from_email,
        )
        event.add_custom("send_provider", "resend")
        event.add_custom("batch_size_attempted", len(recipients))
        event.add_custom("duration_ms", duration_ms)
        event.error(exception=e)
        event.emit()

        return {
            "success": False,
            "error": str(e),
            "total": len(recipients),
        }


def style_dict_to_css(style: dict) -> str:
    """Convert a Python style dict to inline CSS string."""
    if not style:
        return ""

    css_parts = []
    for key, value in style.items():
        # Convert camelCase to kebab-case
        css_key = re.sub(r'([A-Z])', r'-\1', key).lower()
        css_parts.append(f"{css_key}: {value}")

    return "; ".join(css_parts)


def component_to_html(component, base_url: str = "") -> str:
    """
    Convert a dash_email component to HTML string.

    Args:
        component: A dash_email component instance
        base_url: Base URL for converting relative image paths to absolute

    Returns:
        HTML string representation
    """
    if component is None:
        return ""

    # Handle string/text content
    if isinstance(component, str):
        return component

    if isinstance(component, (int, float)):
        return str(component)

    # Handle lists of components
    if isinstance(component, list):
        return "".join(component_to_html(c, base_url) for c in component)

    # Get component type name
    component_type = type(component).__name__

    # Get common properties
    style = getattr(component, 'style', None) or {}
    children = getattr(component, 'children', None)
    css_style = style_dict_to_css(style)
    style_attr = f' style="{css_style}"' if css_style else ""

    # Convert children recursively
    children_html = ""
    if children is not None:
        children_html = component_to_html(children, base_url)

    # Handle each component type
    if component_type == "Email":
        lang = getattr(component, 'lang', 'en') or 'en'
        return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Email</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
</head>
{children_html}
</html>"""

    elif component_type == "EmailBody":
        default_style = "margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<body style="{combined_style}">\n{children_html}\n</body>'

    elif component_type == "EmailContainer":
        default_style = "max-width: 600px; margin: 0 auto;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<div style="{combined_style}">\n{children_html}\n</div>'

    elif component_type == "EmailSection":
        return f'<div{style_attr}>\n{children_html}\n</div>'

    elif component_type == "EmailRow":
        default_style = "display: table; width: 100%; table-layout: fixed;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<div style="{combined_style}">\n{children_html}\n</div>'

    elif component_type == "EmailColumn":
        default_style = "display: table-cell; vertical-align: top;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<div style="{combined_style}">\n{children_html}\n</div>'

    elif component_type == "EmailHeading":
        as_tag = getattr(component, 'as_', 'h1') or 'h1'
        # Also check for 'as' attribute (React prop name)
        if not as_tag or as_tag == 'h1':
            as_tag = getattr(component, 'as', 'h1') or 'h1'
        default_style = "margin: 0;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<{as_tag} style="{combined_style}">{children_html}</{as_tag}>'

    elif component_type == "EmailText":
        default_style = "margin: 16px 0;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<p style="{combined_style}">{children_html}</p>'

    elif component_type == "EmailButton":
        href = getattr(component, 'href', '#') or '#'
        default_style = "display: inline-block; text-decoration: none;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<a href="{href}" style="{combined_style}" target="_blank">{children_html}</a>'

    elif component_type == "EmailLink":
        href = getattr(component, 'href', '#') or '#'
        default_style = "text-decoration: underline;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<a href="{href}" style="{combined_style}">{children_html}</a>'

    elif component_type == "EmailImage":
        src = getattr(component, 'src', '') or ''
        alt = getattr(component, 'alt', '') or ''
        width = getattr(component, 'width', None)
        height = getattr(component, 'height', None)

        # Convert relative URLs to absolute if base_url provided
        if base_url and src.startswith('/'):
            src = f"{base_url}{src}"

        attrs = [f'src="{src}"', f'alt="{alt}"']
        if width:
            attrs.append(f'width="{width}"')
        if height:
            attrs.append(f'height="{height}"')

        default_style = "display: block; border: 0; outline: none;"
        combined_style = f"{default_style} {css_style}".strip()
        attrs.append(f'style="{combined_style}"')

        return f'<img {" ".join(attrs)} />'

    elif component_type == "EmailDivider":
        default_style = "border: none; border-top: 1px solid #eaeaea; margin: 20px 0;"
        combined_style = f"{default_style} {css_style}".strip()
        return f'<hr style="{combined_style}" />'

    elif component_type == "EmailPreview":
        # Preview text is hidden but read by email clients
        return f'<div style="display: none; max-height: 0; overflow: hidden;">{children_html}</div>'

    elif component_type == "EmailHead":
        return f'<head>\n{children_html}\n</head>'

    elif component_type == "EmailFont":
        # Font component generates @font-face CSS
        font_family = getattr(component, 'fontFamily', None)
        web_font = getattr(component, 'webFont', None)
        if font_family and web_font:
            return f"""<style>
@font-face {{
    font-family: '{font_family}';
    src: url('{web_font}');
}}
</style>"""
        return ""

    # Fallback for unknown components - try to render as div
    else:
        return f'<div{style_attr}>{children_html}</div>'


def generate_html_from_code(full_code: str, base_url: str = "") -> str:
    """
    Generate HTML from the dash_email Python code.

    Args:
        full_code: The full Python code string containing email definition
        base_url: Base URL for the server (for image URLs)

    Returns:
        Complete HTML string ready for email sending
    """
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        import dash_email as de
        from dash_iconify import DashIconify

        # Create execution environment
        local_vars = {"de": de, "DashIconify": DashIconify}

        # Execute the code
        exec(full_code, {"de": de, "DashIconify": DashIconify}, local_vars)

        # Get the email component
        email_component = local_vars.get("email")

        if email_component is None:
            html = generate_fallback_html("No email component found in code")
            duration_ms = (time.time() - start_time) * 1000

            # Log partial success (no component found)
            event = email_logger.logger.create_event("email", "email.html_generated")
            event.set_email(
                html_size_bytes=len(html),
                generation_method="code_execution",
            )
            event.add_custom("code_length", len(full_code))
            event.add_custom("duration_ms", duration_ms)
            event.partial("No email component found in code")
            event.emit()

            return html

        # Convert to HTML
        html = component_to_html(email_component, base_url)
        duration_ms = (time.time() - start_time) * 1000

        # Log successful HTML generation
        event = email_logger.logger.create_event("email", "email.html_generated")
        event.set_email(
            html_size_bytes=len(html),
            generation_method="code_execution",
        )
        event.add_custom("code_length", len(full_code))
        event.add_custom("duration_ms", duration_ms)
        event.success()
        event.emit()

        return html

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        html = generate_fallback_html(str(e))

        # Log failed HTML generation
        event = email_logger.logger.create_event("email", "email.html_generated")
        event.set_email(
            html_size_bytes=len(html),
            generation_method="code_execution",
        )
        event.add_custom("code_length", len(full_code))
        event.add_custom("duration_ms", duration_ms)
        event.error(exception=e)
        event.emit()

        print(f"Error generating HTML: {e}")
        return html


def generate_fallback_html(error_message: str = "") -> str:
    """Generate a fallback HTML when conversion fails."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
        <p style="color: #666;">This email was generated with Dash Email.</p>
        {f'<p style="color: #999; font-size: 12px;">Note: {error_message}</p>' if error_message else ''}
    </div>
</body>
</html>"""


# Keep backwards compatibility
def generate_html_from_preview(preview_code: str) -> str:
    """
    Legacy function - generates HTML from preview code.
    Use generate_html_from_code() for better results.
    """
    # Wrap preview code to make it executable
    full_code = f"import dash_email as de\n\nemail = {preview_code}"
    return generate_html_from_code(full_code)
