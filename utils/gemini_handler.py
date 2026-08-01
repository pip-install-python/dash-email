"""
Gemini AI Handler for email generation.
Uses Google's Gemini API to generate email content and dash_email code.
"""
import time
from dotenv import load_dotenv
from google import genai

from utils.ai_config import get_api_key, is_ai_enabled  # noqa: F401  (re-exported)
from utils.wide_event_logger import get_email_logger

# Load environment variables from .env file
load_dotenv()

_client = None


def get_client():
    """
    Build the Gemini client on first use.

    Constructing this at import time raised ValueError whenever no key was set,
    which took down the whole app at startup. Deferring it keeps the app
    importable without a key so the builder can fall back to showcase templates.
    """
    global _client
    if _client is None:
        api_key = get_api_key()
        if not api_key:
            raise RuntimeError(
                "No Gemini API key configured. Set GOOGLE_API_KEY or "
                "GEMINI_API_KEY to enable AI generation."
            )
        _client = genai.Client(api_key=api_key)
    return _client


# Email type descriptions for better prompts
EMAIL_TYPE_DESCRIPTIONS = {
    "promotional": "A promotional email announcing sales, discounts, new products, or special offers. Should be engaging and action-oriented.",
    "welcome": "A welcome email greeting new subscribers or customers. Should be warm, friendly, and set expectations for the relationship.",
    "abandoned_cart": "An abandoned cart reminder email encouraging users to complete their purchase. Should create urgency while being helpful.",
    "re_engagement": "A re-engagement email to win back inactive subscribers. Should offer value or incentives to return.",
    "lead_nurturing": "A lead nurturing email that educates potential customers. Should build trust and guide toward a purchase decision.",
    "newsletter": "A newsletter with valuable content, news, or tips. Should be informative and engaging.",
    "transactional": "A transactional email triggered by a user action like order confirmation or shipping notification. Should be clear and informative.",
    "onboarding": "An onboarding email guiding new users through a product or service. Should be helpful and step-by-step.",
    "feedback": "A feedback or survey request email. Should be polite and explain the value of their input.",
    "announcement": "An announcement email sharing important company news or updates. Should be clear and professional.",
    "milestone": "A milestone celebration email for user achievements or anniversaries. Should be celebratory and appreciative.",
    "personal": "A personal informal email for friends and family. Should be warm and conversational.",
    "professional": "A professional formal email for work communications. Should be clear, concise, and professional.",
    "follow_up": "A follow-up email after initial contact. Should be polite and provide context.",
    "thank_you": "A thank you email expressing gratitude. Should be sincere and specific.",
    "educational": "An educational email teaching about a topic. Should be informative and valuable.",
    "invitation": "An invitation email for events, webinars, or meetings. Should be clear about details and exciting.",
}


def generate_email_content(
    email_type: str,
    user_content: str,
    image_urls: list = None,
) -> dict:
    """
    Generate email content using Gemini AI.

    Args:
        email_type: Type of email to generate
        user_content: User's text content/requirements
        image_urls: Optional list of image URLs (local paths like /assets/uploads/...)

    Returns:
        dict with 'preview_code', 'full_code', and 'subject'
    """
    type_description = EMAIL_TYPE_DESCRIPTIONS.get(
        email_type.lower().replace(" ", "_").replace("-", "_"),
        "A professional email"
    )

    # Build image URL section for prompt
    image_section = ""
    if image_urls and len(image_urls) > 0:
        image_list = "\n".join([f"  - {url}" for url in image_urls])
        image_section = f"""
USER UPLOADED IMAGES (use these exact URLs in EmailImage components):
{image_list}

IMPORTANT: Use these uploaded image URLs in your email design where appropriate.
"""

    # Build the prompt with strict formatting instructions
    prompt = f"""You are an expert email designer. Generate a professional email template using dash_email components.

EMAIL TYPE: {email_type}
DESCRIPTION: {type_description}

USER REQUIREMENTS:
{user_content if user_content else "Create a professional template with placeholder content."}
{image_section}
CRITICAL SYNTAX RULES - YOU MUST FOLLOW THESE EXACTLY:

1. All children must be passed as a list to the `children` parameter
2. Use `children=[...]` syntax for ALL components with children
3. The entire email structure must be properly nested
4. Use `as_="h1"` (with underscore) for EmailHeading, NOT `as="h1"`
5. All style values must use camelCase (backgroundColor, fontSize, etc.)

6. **NEVER USE RAW HTML IN CHILDREN** - This is critical!
   - WRONG: children='<span style="font-size: 28px;">$75.00</span>'
   - WRONG: children='<strong>FREE SHIPPING</strong>'
   - RIGHT: Use separate EmailText components with style props

7. For styled text (prices, emphasis, etc.), use separate EmailText components:
   - Price example: de.EmailText(children="$75.00", style={{"fontSize": "28px", "fontWeight": "bold", "color": "#007bff"}})
   - Bold text: de.EmailText(children="FREE SHIPPING", style={{"fontWeight": "bold", "color": "#28a745"}})

AVAILABLE COMPONENTS:
- de.Email(children=[...], lang="en", style={{}})
- de.EmailBody(children=[...], style={{}})
- de.EmailContainer(children=[...], style={{}})
- de.EmailSection(children=[...], style={{}})
- de.EmailRow(children=[...], style={{}})
- de.EmailColumn(children=[...], style={{}})
- de.EmailHeading(children="text", as_="h1", style={{}})  # NOTE: use as_ not as
- de.EmailText(children="text", style={{}})  # Plain text only, use style for formatting
- de.EmailButton(children="text", href="url", style={{}})
- de.EmailLink(children="text", href="url", style={{}})
- de.EmailImage(src="url", alt="", width=100, style={{}})
- de.EmailDivider(style={{}})
- de.EmailPreview(children="preview text")

CORRECT STRUCTURE EXAMPLE:
```python
import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="Preview text here"),
        de.EmailBody(
            style={{"backgroundColor": "#f6f9fc"}},
            children=[
                de.EmailContainer(
                    style={{"padding": "40px 20px"}},
                    children=[
                        de.EmailSection(
                            style={{"backgroundColor": "#ffffff", "padding": "30px", "borderRadius": "8px"}},
                            children=[
                                de.EmailHeading(
                                    children="Welcome!",
                                    as_="h1",
                                    style={{"color": "#333333", "fontSize": "28px", "margin": "0 0 20px 0"}}
                                ),
                                de.EmailText(
                                    children="Thank you for joining us.",
                                    style={{"color": "#666666", "fontSize": "16px", "lineHeight": "24px"}}
                                ),
                                # For styled text like prices, use style prop NOT HTML:
                                de.EmailText(
                                    children="$99.00",
                                    style={{"fontSize": "32px", "fontWeight": "bold", "color": "#007bff", "margin": "10px 0"}}
                                ),
                                de.EmailText(
                                    children="+ FREE SHIPPING!",
                                    style={{"fontSize": "16px", "fontWeight": "bold", "color": "#28a745"}}
                                ),
                                de.EmailButton(
                                    children="Get Started",
                                    href="https://example.com",
                                    style={{"backgroundColor": "#007bff", "color": "#ffffff", "padding": "12px 24px", "borderRadius": "6px", "textDecoration": "none"}}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
```

Generate the email now. Return ONLY in this exact format:

SUBJECT: [Your subject line]

FULL_CODE:
```python
import dash_email as de

email = de.Email(
    # Your complete, properly nested email here
)
```
"""

    # Build content parts (text only, images are referenced by URL)
    content_parts = [prompt]

    # Get logger for tracking
    email_logger = get_email_logger()
    start_time = time.time()

    try:
        response = get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=content_parts,
        )

        response_text = response.text
        duration_ms = (time.time() - start_time) * 1000

        # Parse the response
        result = {
            "subject": "",
            "full_code": "",
            "preview_code": "",
            "raw_response": response_text,
        }

        # Extract subject
        if "SUBJECT:" in response_text:
            subject_start = response_text.find("SUBJECT:") + 8
            subject_end = response_text.find("\n", subject_start)
            result["subject"] = response_text[subject_start:subject_end].strip()

        # Extract full code
        code_valid = False
        if "```python" in response_text:
            code_start = response_text.find("```python") + 9
            code_end = response_text.find("```", code_start)
            full_code = response_text[code_start:code_end].strip()
            result["full_code"] = full_code
            code_valid = "de.Email" in full_code

            # Generate preview code - extract just the de.Email(...) expression
            preview_lines = []
            in_email = False
            paren_depth = 0

            for line in full_code.split("\n"):
                # Skip import lines
                if line.strip().startswith("import"):
                    continue

                # Start capturing from "email = de.Email(" or "de.Email("
                if not in_email:
                    if "email = de.Email(" in line:
                        # Remove "email = " and start capturing
                        line = line.replace("email = ", "")
                        in_email = True
                    elif line.strip().startswith("de.Email("):
                        in_email = True

                if in_email:
                    preview_lines.append(line)
                    # Track parentheses to know when the expression ends
                    paren_depth += line.count("(") - line.count(")")

            result["preview_code"] = "\n".join(preview_lines).strip()

        # Log successful AI call
        event = email_logger.logger.create_event("ai", "ai.email_generated")
        event.set_ai(
            model="gemini-2.5-flash",
            prompt_length=len(prompt),
            response_length=len(response_text),
        )
        event.add_custom("ai_email_type", email_type)
        event.add_custom("ai_has_images", bool(image_urls))
        event.add_custom("ai_image_count", len(image_urls) if image_urls else 0)
        event.add_custom("ai_has_code", "```python" in response_text)
        event.add_custom("ai_code_valid", code_valid)
        event.add_custom("duration_ms", duration_ms)
        event.success()
        event.emit()

        return result

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Log failed AI call
        event = email_logger.logger.create_event("ai", "ai.email_generated")
        event.set_ai(
            model="gemini-2.5-flash",
            prompt_length=len(prompt),
        )
        event.add_custom("ai_email_type", email_type)
        event.add_custom("ai_has_images", bool(image_urls))
        event.add_custom("duration_ms", duration_ms)
        event.error(exception=e)
        event.emit()

        return {
            "subject": "Error generating email",
            "full_code": f"# Error: {str(e)}",
            "preview_code": f"# Error: {str(e)}",
            "raw_response": str(e),
            "error": str(e),
        }
