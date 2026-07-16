"""
Wide Event Logger for dash-email.

Implements the "Wide Events" / "Canonical Log Lines" pattern for structured,
high-cardinality, high-dimensionality logging. One comprehensive event per
operation instead of scattered log statements.

Reference: https://loggingsucks.com
"""
import os
import json
import time
import uuid
import random
import logging
from enum import Enum
from datetime import datetime
from typing import Optional, Any, Dict
from dataclasses import dataclass, field
from contextlib import contextmanager

# Standard logger for fallback
logger = logging.getLogger("dash-email")


class LoggerMode(Enum):
    """Logging mode configuration."""
    DEBUG = "debug"   # 100% of events, pretty output
    TAIL = "tail"     # Tail-based sampling (errors + 5% success)
    NONE = "none"     # Disabled


class Severity(Enum):
    """Log severity levels."""
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Outcome(Enum):
    """Operation outcome."""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


def get_logger_mode() -> LoggerMode:
    """
    Get logger mode from environment.

    Priority:
    1. LOGGER_MODE env var
    2. DEBUG=true → debug mode
    3. Default to tail mode
    """
    mode_str = os.getenv("LOGGER_MODE", "").lower()

    if mode_str == "debug":
        return LoggerMode.DEBUG
    elif mode_str == "tail":
        return LoggerMode.TAIL
    elif mode_str == "none":
        return LoggerMode.NONE

    # Default: debug if DEBUG=true, otherwise tail
    if os.getenv("DEBUG", "").lower() == "true":
        return LoggerMode.DEBUG

    return LoggerMode.TAIL


def _safe_serialize(value: Any) -> Any:
    """
    Safely serialize any Python object for JSON.

    Handles:
    - Primitives (str, int, float, bool, None)
    - Enums → value
    - datetime → ISO format
    - dicts/lists → recursive
    - Exceptions → {type, message}
    - Unknown → str() fallback
    """
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, dict):
        return {k: _safe_serialize(v) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return [_safe_serialize(v) for v in value]

    if isinstance(value, Exception):
        return {
            "type": type(value).__name__,
            "message": str(value),
        }

    # Fallback to string representation
    try:
        return str(value)
    except Exception:
        return f"<unserializable: {type(value).__name__}>"


@dataclass
class WideEvent:
    """
    A single wide event with fluent API for building comprehensive logs.

    Usage:
        event = WideEvent(domain="email", name="email.sent")
        event.set_email(type="promotional", recipient="user@example.com")
        event.set_ai(model="gemini-2.5-flash", tokens=2300)
        event.success()
        event.emit()
    """

    # Core fields (set at creation)
    event_domain: str
    event_name: str

    # Auto-generated fields
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    # Classification (set via methods)
    severity: Severity = Severity.INFO
    outcome: Outcome = Outcome.SUCCESS

    # Service context
    service_name: str = "dash-email"
    service_version: str = "1.0.0"

    # Timing
    start_time: float = field(default_factory=time.time)
    duration_ms: Optional[float] = None

    # Dynamic attributes
    attributes: Dict[str, Any] = field(default_factory=dict)

    # Error context
    error_type: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    error_retriable: bool = False

    # Logger reference (set by WideEventLogger)
    _logger: Optional["WideEventLogger"] = field(default=None, repr=False)

    def set_email(
        self,
        type: Optional[str] = None,
        subject: Optional[str] = None,
        recipient: Optional[str] = None,
        from_addr: Optional[str] = None,
        component_count: Optional[int] = None,
        image_count: Optional[int] = None,
        html_size_bytes: Optional[int] = None,
        generation_method: Optional[str] = None,
    ) -> "WideEvent":
        """Set email-related fields."""
        if type:
            self.attributes["email_type"] = type
        if subject:
            self.attributes["email_subject"] = subject
        if recipient:
            self.attributes["email_recipient"] = recipient
        if from_addr:
            self.attributes["email_from"] = from_addr
        if component_count is not None:
            self.attributes["component_count"] = component_count
        if image_count is not None:
            self.attributes["image_count"] = image_count
        if html_size_bytes is not None:
            self.attributes["html_size_bytes"] = html_size_bytes
        if generation_method:
            self.attributes["generation_method"] = generation_method
        return self

    def set_ai(
        self,
        model: Optional[str] = None,
        provider: str = "google",
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        cost_usd: Optional[float] = None,
        prompt_length: Optional[int] = None,
        response_length: Optional[int] = None,
    ) -> "WideEvent":
        """Set AI/Gemini-related fields."""
        if model:
            self.attributes["ai_model"] = model
        self.attributes["ai_provider"] = provider
        if input_tokens is not None:
            self.attributes["ai_input_tokens"] = input_tokens
        if output_tokens is not None:
            self.attributes["ai_output_tokens"] = output_tokens
        if total_tokens is not None:
            self.attributes["ai_total_tokens"] = total_tokens
        elif input_tokens is not None and output_tokens is not None:
            self.attributes["ai_total_tokens"] = input_tokens + output_tokens
        if cost_usd is not None:
            self.attributes["ai_cost_usd"] = cost_usd
        if prompt_length is not None:
            self.attributes["ai_prompt_length"] = prompt_length
        if response_length is not None:
            self.attributes["ai_response_length"] = response_length
        return self

    def set_storage(
        self,
        image_count: Optional[int] = None,
        total_bytes: Optional[int] = None,
        image_types: Optional[list] = None,
        files_cleaned: Optional[int] = None,
        bytes_freed: Optional[int] = None,
    ) -> "WideEvent":
        """Set storage/image-related fields."""
        if image_count is not None:
            self.attributes["image_count"] = image_count
        if total_bytes is not None:
            self.attributes["image_total_bytes"] = total_bytes
        if image_types:
            self.attributes["image_types"] = image_types
        if files_cleaned is not None:
            self.attributes["storage_files_cleaned"] = files_cleaned
        if bytes_freed is not None:
            self.attributes["storage_bytes_freed"] = bytes_freed
        return self

    def add_custom(self, key: str, value: Any) -> "WideEvent":
        """Add any custom field (safely serialized)."""
        self.attributes[key] = _safe_serialize(value)
        return self

    def success(self) -> "WideEvent":
        """Mark event as successful."""
        self.outcome = Outcome.SUCCESS
        self.severity = Severity.INFO
        return self

    def partial(self, reason: Optional[str] = None) -> "WideEvent":
        """Mark event as partially successful (warning)."""
        self.outcome = Outcome.PARTIAL
        self.severity = Severity.WARN
        if reason:
            self.attributes["partial_reason"] = reason
        return self

    def error(
        self,
        error_type: Optional[str] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        retriable: bool = False,
        exception: Optional[Exception] = None,
    ) -> "WideEvent":
        """Mark event as failed with error details."""
        self.outcome = Outcome.FAILURE
        self.severity = Severity.ERROR

        if exception:
            self.error_type = type(exception).__name__
            self.error_message = str(exception)
        else:
            self.error_type = error_type
            self.error_message = error_message

        self.error_code = error_code
        self.error_retriable = retriable
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for JSON serialization."""
        # Calculate duration if not set
        if self.duration_ms is None:
            self.duration_ms = (time.time() - self.start_time) * 1000

        data = {
            # Core fields
            "event_id": self.event_id,
            "event_domain": self.event_domain,
            "event_name": self.event_name,
            "timestamp": self.timestamp,

            # Classification
            "severity": self.severity.value,
            "outcome": self.outcome.value,

            # Service context
            "service_name": self.service_name,
            "service_version": self.service_version,

            # Timing
            "duration_ms": round(self.duration_ms, 2),
        }

        # Add error fields if present
        if self.error_type:
            data["error_type"] = self.error_type
        if self.error_code:
            data["error_code"] = self.error_code
        if self.error_message:
            data["error_message"] = self.error_message
        if self.outcome == Outcome.FAILURE:
            data["error_retriable"] = self.error_retriable

        # Add all custom attributes
        data.update(self.attributes)

        return data

    def emit(self) -> None:
        """Emit the event through the logger."""
        if self._logger:
            self._logger.emit(self)
        else:
            # Fallback: print to console
            self._print_event()

    def _print_event(self) -> None:
        """Print event to console (debug mode)."""
        data = self.to_dict()
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Summary line
        summary = (
            f"{timestamp} [WIDE-EVENT] [{self.event_domain}:{self.event_name}] "
            f"outcome={self.outcome.value} duration={round(self.duration_ms or 0)}ms"
        )
        print(summary)

        # Full JSON (pretty)
        print(json.dumps(data, indent=2, default=str))


class DebugSampler:
    """Keep 100% of events - for development."""

    def should_emit(self, event: WideEvent) -> bool:
        return True


class TailSampler:
    """
    Intelligent tail-based sampling for production.

    ALWAYS keeps:
    - Errors and failures
    - Slow requests (> 3000ms)
    - Partial failures
    - AI calls (for cost tracking)
    - Email sends (important operations)

    Samples success at 5%.
    """

    def __init__(self, success_sample_rate: float = 0.05):
        self.success_sample_rate = success_sample_rate

    def should_emit(self, event: WideEvent) -> bool:
        # ALWAYS keep errors
        if event.outcome == Outcome.FAILURE:
            return True
        if event.severity in (Severity.ERROR, Severity.FATAL):
            return True

        # ALWAYS keep slow requests
        if event.duration_ms and event.duration_ms > 3000:
            return True

        # ALWAYS keep partial failures
        if event.outcome == Outcome.PARTIAL:
            return True

        # ALWAYS keep AI calls (for cost tracking)
        if event.attributes.get("ai_model"):
            return True

        # ALWAYS keep email sends
        if event.attributes.get("email_recipient"):
            return True

        # Sample success at configured rate
        return random.random() < self.success_sample_rate


class NullSampler:
    """Emit nothing - for when logging is disabled."""

    def should_emit(self, event: WideEvent) -> bool:
        return False


class WideEventLogger:
    """
    Main Wide Event logger.

    Handles event creation, sampling, and emission based on LOGGER_MODE.
    """

    def __init__(self, mode: Optional[LoggerMode] = None):
        self.mode = mode or get_logger_mode()

        if self.mode == LoggerMode.DEBUG:
            self.sampler = DebugSampler()
        elif self.mode == LoggerMode.TAIL:
            self.sampler = TailSampler()
        else:
            self.sampler = NullSampler()

        logger.info(f"Wide Event Logger initialized in {self.mode.value} mode")

    def create_event(self, domain: str, name: str) -> WideEvent:
        """Create a new wide event."""
        event = WideEvent(event_domain=domain, event_name=name)
        event._logger = self
        return event

    def emit(self, event: WideEvent) -> None:
        """Emit an event (subject to sampling)."""
        if not self.sampler.should_emit(event):
            return

        # Calculate duration if not set
        if event.duration_ms is None:
            event.duration_ms = (time.time() - event.start_time) * 1000

        data = event.to_dict()

        if self.mode == LoggerMode.DEBUG:
            # Pretty print for development
            timestamp = datetime.now().strftime("%H:%M:%S")
            summary = (
                f"{timestamp} [WIDE-EVENT] [{event.event_domain}:{event.event_name}] "
                f"outcome={event.outcome.value} duration={round(event.duration_ms)}ms"
            )
            print(summary)
            print(json.dumps(data, indent=2, default=str))
        else:
            # Compact JSON for production (one line per event)
            print(json.dumps(data, default=str))


class EmailEventLogger:
    """
    Email-specific event logger with convenient context managers.

    Usage:
        email_logger = get_email_logger()

        with email_logger.email_generation(email_type="promotional") as event:
            event.set_ai(model="gemini-2.5-flash", tokens=2300)
            result = generate(...)
            event.success()
    """

    def __init__(self, logger: Optional[WideEventLogger] = None):
        self.logger = logger or WideEventLogger()

    @contextmanager
    def email_generation(self, email_type: str, **kwargs):
        """Context manager for email generation operations."""
        event = self.logger.create_event("email", "email.generated")
        event.set_email(type=email_type, generation_method="ai")

        for key, value in kwargs.items():
            event.add_custom(key, value)

        try:
            yield event
        except Exception as e:
            event.error(exception=e)
            raise
        finally:
            event.emit()

    @contextmanager
    def email_send(self, recipient: str, subject: str, **kwargs):
        """Context manager for sending emails."""
        event = self.logger.create_event("email", "email.sent")
        event.set_email(recipient=recipient, subject=subject)

        for key, value in kwargs.items():
            event.add_custom(key, value)

        try:
            yield event
        except Exception as e:
            event.error(exception=e)
            raise
        finally:
            event.emit()

    @contextmanager
    def email_preview(self, email_type: str = None, **kwargs):
        """Context manager for email preview generation."""
        event = self.logger.create_event("email", "email.preview")
        if email_type:
            event.set_email(type=email_type)

        for key, value in kwargs.items():
            event.add_custom(key, value)

        try:
            yield event
        except Exception as e:
            event.error(exception=e)
            raise
        finally:
            event.emit()

    @contextmanager
    def image_upload(self, image_count: int = 0, **kwargs):
        """Context manager for image upload operations."""
        event = self.logger.create_event("storage", "image.uploaded")
        event.set_storage(image_count=image_count)

        for key, value in kwargs.items():
            event.add_custom(key, value)

        try:
            yield event
        except Exception as e:
            event.error(exception=e)
            raise
        finally:
            event.emit()

    @contextmanager
    def image_cleanup(self, **kwargs):
        """Context manager for image cleanup operations."""
        event = self.logger.create_event("storage", "image.cleanup")

        for key, value in kwargs.items():
            event.add_custom(key, value)

        try:
            yield event
        except Exception as e:
            event.error(exception=e)
            raise
        finally:
            event.emit()

    @contextmanager
    def ai_call(self, model: str = "gemini-2.5-flash", email_type: str = None, **kwargs):
        """Context manager for AI API calls."""
        event = self.logger.create_event("ai", "ai.email_generated")
        event.set_ai(model=model)

        if email_type:
            event.attributes["ai_email_type"] = email_type

        for key, value in kwargs.items():
            event.add_custom(key, value)

        try:
            yield event
        except Exception as e:
            event.error(exception=e)
            raise
        finally:
            event.emit()


# Singleton instance
_email_logger: Optional[EmailEventLogger] = None


def get_email_logger() -> EmailEventLogger:
    """Get the singleton EmailEventLogger instance."""
    global _email_logger
    if _email_logger is None:
        _email_logger = EmailEventLogger()
    return _email_logger


def get_wide_event_logger() -> WideEventLogger:
    """Get the underlying WideEventLogger instance."""
    return get_email_logger().logger
