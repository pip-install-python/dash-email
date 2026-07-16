"""
Resend Templates API Handler.
Provides functions to create, manage, and send emails using Resend templates.
"""
import os
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv
import resend

from utils.wide_event_logger import get_email_logger

# Load environment variables
load_dotenv()

# Initialize Resend with API key
resend.api_key = os.getenv("RESEND_API_KEY")


def create_template(
    name: str,
    subject: str,
    html: str,
    from_email: str = "onboarding@resend.dev",
    variables: Optional[List[Dict]] = None,
) -> dict:
    """
    Create a template in Resend.

    Args:
        name: Template name (for identification)
        subject: Email subject line
        html: HTML content with optional variables like {{{NAME}}}
        from_email: Sender email address
        variables: Optional list of variable definitions:
            [{"key": "NAME", "type": "string", "fallback_value": "Customer"}]

    Reserved variable names (cannot use):
        - FIRST_NAME, LAST_NAME, EMAIL
        - RESEND_UNSUBSCRIBE_URL
        - contact, this

    Returns:
        dict with template_id and status
    """
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        params = {
            "name": name,
            "subject": subject,
            "html": html,
            "from": from_email,
        }

        if variables:
            params["variables"] = variables

        result = resend.Templates.create(params)
        duration_ms = (time.time() - start_time) * 1000

        # Log successful template creation
        event = email_logger.logger.create_event("email", "template.created")
        event.add_custom("template_name", name)
        event.add_custom("template_id", result.get("id", "N/A"))
        event.add_custom("has_variables", variables is not None)
        event.add_custom("variable_count", len(variables) if variables else 0)
        event.add_custom("html_size_bytes", len(html))
        event.add_custom("duration_ms", duration_ms)
        event.success()
        event.emit()

        return {
            "success": True,
            "template_id": result.get("id"),
            "message": f"Template '{name}' created successfully!",
            "data": result,
        }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Log failed template creation
        event = email_logger.logger.create_event("email", "template.created")
        event.add_custom("template_name", name)
        event.add_custom("duration_ms", duration_ms)
        event.error(exception=e)
        event.emit()

        return {
            "success": False,
            "error": str(e),
        }


def list_templates() -> dict:
    """
    List all templates in Resend account.

    Returns:
        dict with list of templates or error
    """
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        result = resend.Templates.list()
        duration_ms = (time.time() - start_time) * 1000

        # Resend returns a dict with 'data' key containing list of templates
        templates = result.get("data", []) if isinstance(result, dict) else result

        # Log successful list
        event = email_logger.logger.create_event("email", "template.listed")
        event.add_custom("template_count", len(templates))
        event.add_custom("duration_ms", duration_ms)
        event.success()
        event.emit()

        return {
            "success": True,
            "templates": templates,
            "count": len(templates),
        }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Log failed list
        event = email_logger.logger.create_event("email", "template.listed")
        event.add_custom("duration_ms", duration_ms)
        event.error(exception=e)
        event.emit()

        return {
            "success": False,
            "error": str(e),
            "templates": [],
        }


def get_template(template_id: str) -> dict:
    """
    Get a template by ID.

    Args:
        template_id: Resend template ID

    Returns:
        dict with template data or error
    """
    try:
        result = resend.Templates.get(template_id)
        return {
            "success": True,
            "template": result,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def delete_template(template_id: str) -> dict:
    """
    Delete a template.

    Args:
        template_id: Resend template ID

    Returns:
        dict with success status or error
    """
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        result = resend.Templates.remove(template_id)
        duration_ms = (time.time() - start_time) * 1000

        # Log successful deletion
        event = email_logger.logger.create_event("email", "template.deleted")
        event.add_custom("template_id", template_id)
        event.add_custom("duration_ms", duration_ms)
        event.success()
        event.emit()

        return {
            "success": True,
            "message": f"Template {template_id} deleted successfully!",
            "data": result,
        }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Log failed deletion
        event = email_logger.logger.create_event("email", "template.deleted")
        event.add_custom("template_id", template_id)
        event.add_custom("duration_ms", duration_ms)
        event.error(exception=e)
        event.emit()

        return {
            "success": False,
            "error": str(e),
        }


def send_with_template(
    to_email: str,
    template_id: str,
    template_data: Optional[Dict] = None,
    from_email: str = "onboarding@resend.dev",
    scheduled_at: Optional[str] = None,
) -> dict:
    """
    Send email using a Resend template.

    Args:
        to_email: Recipient email address
        template_id: Resend template ID
        template_data: Dict of variable values, e.g., {"NAME": "John", "TOTAL": 99.99}
        from_email: Sender email address
        scheduled_at: Optional schedule time (ISO 8601 or natural language)

    Returns:
        dict with success status and email ID
    """
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        params = {
            "from": from_email,
            "to": [to_email],
            "template_id": template_id,
        }

        if template_data:
            params["template_data"] = template_data

        if scheduled_at:
            params["scheduled_at"] = scheduled_at

        result = resend.Emails.send(params)
        duration_ms = (time.time() - start_time) * 1000

        # Log successful send
        event = email_logger.logger.create_event("email", "email.sent")
        event.set_email(
            recipient=to_email,
            from_addr=from_email,
        )
        event.add_custom("send_provider", "resend")
        event.add_custom("email_id", result.get("id", "N/A"))
        event.add_custom("template_id", template_id)
        event.add_custom("used_template", True)
        event.add_custom("has_template_data", template_data is not None)
        event.add_custom("scheduled", scheduled_at is not None)
        event.add_custom("duration_ms", duration_ms)
        event.success()
        event.emit()

        message = f"Email sent using template! ID: {result.get('id', 'N/A')}"
        if scheduled_at:
            message = f"Email scheduled using template! ID: {result.get('id', 'N/A')}"

        return {
            "success": True,
            "message": message,
            "email_id": result.get("id"),
            "response": result,
        }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Log failed send
        event = email_logger.logger.create_event("email", "email.sent")
        event.set_email(
            recipient=to_email,
            from_addr=from_email,
        )
        event.add_custom("send_provider", "resend")
        event.add_custom("template_id", template_id)
        event.add_custom("used_template", True)
        event.add_custom("duration_ms", duration_ms)
        event.error(exception=e)
        event.emit()

        return {
            "success": False,
            "error": str(e),
        }
