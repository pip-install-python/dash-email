# Dash Email - Skills & Knowledge Base

This document provides comprehensive knowledge for building with dash-email, including architecture details, component specifications, styling patterns, and integration guides.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Component Deep Dive](#component-deep-dive)
3. [Styling for Email Clients](#styling-for-email-clients)
4. [Layout Patterns](#layout-patterns)
5. [AI-Powered Generation](#ai-powered-generation)
6. [Email Sending with Resend](#email-sending-with-resend)
7. [Template Management](#template-management)
8. [Image Handling](#image-handling)
9. [Common Recipes](#common-recipes)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)

---

## Architecture Overview

### How dash-email Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        Python (Dash)                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  import dash_email as de                                  │  │
│  │  de.Email(children=[de.EmailBody([...])])                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Python Component Wrappers (dash_email/*.py)              │  │
│  │  - Auto-generated from React components                   │  │
│  │  - Serialize props to JSON                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     JavaScript (Browser)                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  React Components (dash_email.min.js)                     │  │
│  │  - Wraps @react-email/components                          │  │
│  │  - Renders to DOM for preview                             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  HTML Output                                              │  │
│  │  - Email-compatible HTML                                  │  │
│  │  - Table-based layouts                                    │  │
│  │  - Inline styles                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### File Structure

```
dash_email/
├── __init__.py          # Package exports
├── _imports_.py         # Component imports
├── Email.py             # Root component
├── EmailBody.py         # Body wrapper
├── EmailButton.py       # CTA buttons
├── EmailColumn.py       # Table columns
├── EmailContainer.py    # Centered container
├── EmailDivider.py      # Horizontal rules
├── EmailFont.py         # Custom fonts
├── EmailHead.py         # Metadata section
├── EmailHeading.py      # h1-h6 elements
├── EmailImage.py        # Images
├── EmailLink.py         # Hyperlinks
├── EmailPreview.py      # Inbox preview text
├── EmailRow.py          # Table rows
├── EmailSection.py      # Content groups
├── EmailText.py         # Paragraphs
├── dash_email.min.js    # Bundled React
└── metadata.json        # Component metadata
```

---

## Component Deep Dive

### Email (Root Component)

The root wrapper that establishes the email document structure.

```python
de.Email(
    id="my-email",           # Optional: Dash component ID
    lang="en",               # Language code (default: "en")
    dir="ltr",               # Text direction: "ltr" or "rtl"
    style={},                # Custom styles
    children=[]              # Child components
)
```

**Rendered HTML:**
```html
<div lang="en" dir="ltr" data-email-component="html"
     style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <!-- children -->
</div>
```

**Usage Notes:**
- Always wrap your entire email in this component
- Sets default system font stack
- Use `dir="rtl"` for Arabic, Hebrew, etc.

---

### EmailHead

Container for email metadata (fonts, styles). Hidden in preview.

```python
de.EmailHead(
    children=[
        de.EmailFont(
            fontFamily="Roboto",
            webFont={
                "url": "https://fonts.googleapis.com/css2?family=Roboto",
                "format": "woff2"
            }
        )
    ]
)
```

**Usage Notes:**
- Content is hidden (`display: none`)
- Used primarily for `EmailFont` components
- Placed at the start of `Email` children

---

### EmailPreview

Sets the preview text shown in email client inboxes before opening.

```python
de.EmailPreview("Your order has shipped! Track your package...")
```

**Rendered HTML:**
```html
<div style="display:none;font-size:1px;line-height:1px;max-height:0;
            max-width:0;opacity:0;overflow:hidden;">
  Your order has shipped! Track your package...
</div>
```

**Usage Notes:**
- Keep under 150 characters for best display
- Appears after subject line in inbox
- Hidden in the actual email body
- Place early in the Email children

---

### EmailBody

Main content wrapper for the email body.

```python
de.EmailBody(
    style={
        "backgroundColor": "#f6f9fc",
        "padding": "40px 0"
    },
    children=[...]
)
```

**Default Styles Applied:**
- `margin: 0`
- `padding: 0`
- `width: 100%`

---

### EmailContainer

Centers content with a maximum width (industry standard: 600px).

```python
de.EmailContainer(
    style={
        "padding": "20px",
        "backgroundColor": "#ffffff"
    },
    children=[...]
)
```

**Default Styles Applied:**
- `maxWidth: 600px`
- `margin: 0 auto`

**Usage Notes:**
- Use for main content area
- 600px is the email standard for readability
- Can nest multiple containers for different sections

---

### EmailSection

Groups related content together.

```python
de.EmailSection(
    style={
        "padding": "32px",
        "backgroundColor": "#ffffff",
        "borderRadius": "8px"
    },
    children=[
        de.EmailHeading("Section Title", as_="h2"),
        de.EmailText("Section content here...")
    ]
)
```

**Usage Notes:**
- Use for logical content grouping
- Apply background colors and padding here
- Helps organize complex emails

---

### EmailRow & EmailColumn

Create multi-column layouts using table-based structure.

```python
de.EmailRow([
    de.EmailColumn(
        style={"width": "50%", "paddingRight": "12px"},
        children=[de.EmailText("Left column content")]
    ),
    de.EmailColumn(
        style={"width": "50%", "paddingLeft": "12px"},
        children=[de.EmailText("Right column content")]
    )
])
```

**EmailRow Default Styles:**
- `width: 100%`
- `borderCollapse: collapse`

**EmailColumn Default Styles:**
- `verticalAlign: top`

**Rendered HTML:**
```html
<table cellpadding="0" cellspacing="0" border="0" style="width:100%">
  <tbody>
    <tr>
      <td style="vertical-align:top;width:50%">Left column</td>
      <td style="vertical-align:top;width:50%">Right column</td>
    </tr>
  </tbody>
</table>
```

**Usage Notes:**
- Essential for email client compatibility
- Always use percentage widths
- Add padding to columns, not rows
- Maximum 3-4 columns recommended

---

### EmailHeading

Renders heading elements (h1-h6).

```python
de.EmailHeading(
    "Welcome to Our Platform!",
    as_="h1",                    # h1, h2, h3, h4, h5, h6
    style={
        "color": "#1a1a1a",
        "fontSize": "28px",
        "fontWeight": "bold",
        "margin": "0 0 16px 0"
    }
)
```

**Default Styles Applied:**
- `margin: 16px 0`

**Important:** Use `as_` (with underscore) because `as` is a Python reserved keyword.

**Typical Font Sizes:**
| Level | Recommended Size |
|-------|------------------|
| h1    | 28-32px          |
| h2    | 24-26px          |
| h3    | 20-22px          |
| h4    | 18px             |
| h5    | 16px             |
| h6    | 14px             |

---

### EmailText

Renders paragraph text.

```python
de.EmailText(
    "Thank you for your purchase. Your order will arrive in 3-5 business days.",
    style={
        "color": "#666666",
        "fontSize": "16px",
        "lineHeight": "1.6",
        "margin": "0 0 16px 0"
    }
)
```

**Default Styles Applied:**
- `margin: 16px 0`

**Usage Notes:**
- Use for body copy
- Set `lineHeight` for readability (1.5-1.6 recommended)
- Keep paragraphs short (2-3 sentences)

---

### EmailButton

Styled link that appears as a button (CTA).

```python
de.EmailButton(
    "Shop Now",
    href="https://example.com/shop",
    target="_blank",              # Default: "_blank"
    style={
        "backgroundColor": "#007bff",
        "color": "#ffffff",
        "padding": "14px 28px",
        "borderRadius": "6px",
        "fontSize": "16px",
        "fontWeight": "bold",
        "textDecoration": "none"
    }
)
```

**Default Styles Applied:**
- `display: inline-block`
- `textDecoration: none`
- `textAlign: center`

**Button Style Patterns:**

```python
# Primary Button
primary_style = {
    "backgroundColor": "#007bff",
    "color": "#ffffff",
    "padding": "12px 24px",
    "borderRadius": "4px",
    "fontWeight": "bold"
}

# Secondary/Outline Button
secondary_style = {
    "backgroundColor": "transparent",
    "color": "#007bff",
    "padding": "12px 24px",
    "borderRadius": "4px",
    "border": "2px solid #007bff"
}

# Ghost Button
ghost_style = {
    "backgroundColor": "transparent",
    "color": "#333333",
    "padding": "12px 24px",
    "textDecoration": "underline"
}
```

---

### EmailLink

Renders a hyperlink.

```python
de.EmailLink(
    "View our privacy policy",
    href="https://example.com/privacy",
    target="_blank",              # Default: "_blank"
    style={
        "color": "#007bff",
        "textDecoration": "underline"
    }
)
```

**Usage Notes:**
- Use within `EmailText` for inline links
- Always include `href`
- Consider adding `textDecoration: underline` for clarity

---

### EmailImage

Renders an image element.

```python
de.EmailImage(
    src="https://example.com/logo.png",
    alt="Company Logo",           # Default: ""
    width=200,                    # Number or string
    height=50,                    # Number or string
    style={
        "borderRadius": "8px",
        "margin": "0 auto"
    }
)
```

**Default Styles Applied:**
- `display: block`
- `outline: none`
- `border: none`
- `textDecoration: none`

**Usage Notes:**
- Always provide `alt` text for accessibility
- Use absolute URLs for production
- Specify dimensions to prevent layout shift
- Images are blocked by default in many clients

**Image Best Practices:**
```python
# Centered logo
de.EmailImage(
    src="https://cdn.example.com/logo.png",
    alt="Company Name",
    width=150,
    style={"margin": "0 auto", "display": "block"}
)

# Full-width hero image
de.EmailImage(
    src="https://cdn.example.com/hero.jpg",
    alt="Summer Sale - 50% Off",
    width="100%",
    style={"maxWidth": "600px"}
)
```

---

### EmailDivider

Renders a horizontal divider line.

```python
de.EmailDivider(
    style={
        "borderTop": "2px solid #eaeaea",
        "margin": "32px 0"
    }
)
```

**Default Styles Applied:**
- `border: none`
- `borderTop: 1px solid #eaeaea`
- `margin: 16px 0`

---

### EmailFont

Loads custom fonts via @font-face.

```python
de.EmailFont(
    fontFamily="Inter",
    fallbackFontFamily="Helvetica, Arial, sans-serif",  # Default: "Helvetica"
    webFont={
        "url": "https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjp-Ek-_EeA.woff2",
        "format": "woff2"
    },
    fontStyle="normal",          # Default: "normal"
    fontWeight=400               # Default: 400
)
```

**Usage Notes:**
- Place inside `EmailHead`
- Many email clients don't support custom fonts
- Always provide fallback fonts
- Google Fonts work well

---

## Styling for Email Clients

### The Golden Rules

1. **Inline styles only** - External CSS is stripped by most email clients
2. **Use tables for layout** - Flexbox/Grid not widely supported
3. **600px max width** - Standard for readability
4. **Web-safe fonts as fallback** - Custom fonts often blocked
5. **No JavaScript** - Completely ignored

### Supported CSS Properties

**Fully Supported:**
```python
style={
    # Colors
    "color": "#333333",
    "backgroundColor": "#ffffff",

    # Typography
    "fontSize": "16px",
    "fontFamily": "Arial, sans-serif",
    "fontWeight": "bold",
    "fontStyle": "italic",
    "lineHeight": "1.6",
    "textAlign": "center",
    "textDecoration": "underline",

    # Box Model
    "padding": "20px",
    "margin": "10px 0",
    "width": "100%",
    "maxWidth": "600px",

    # Borders
    "border": "1px solid #eaeaea",
    "borderRadius": "8px",  # Limited support
    "borderTop": "2px solid #007bff",

    # Display
    "display": "block",
    "display": "inline-block",
}
```

**Limited/Partial Support:**
```python
style={
    "borderRadius": "8px",       # Outlook ignores
    "boxShadow": "...",          # Many clients ignore
    "backgroundImage": "...",    # Outlook ignores
}
```

**Not Supported:**
```python
# Don't use these
style={
    "display": "flex",           # ❌
    "display": "grid",           # ❌
    "position": "absolute",      # ❌
    "float": "left",             # ❌ (unreliable)
}
```

### Color Formats

```python
# All valid
style={
    "color": "#333333",          # Hex (recommended)
    "color": "#333",             # Short hex
    "color": "rgb(51, 51, 51)",  # RGB
    "color": "black",            # Named colors
}
```

### Font Stacks

```python
# System font stack (recommended)
"fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

# Web-safe serif
"fontFamily": "Georgia, 'Times New Roman', Times, serif"

# Web-safe monospace
"fontFamily": "'Courier New', Courier, monospace"
```

---

## Layout Patterns

### Single Column (Most Common)

```python
de.Email([
    de.EmailBody(
        style={"backgroundColor": "#f6f9fc"},
        children=[
            de.EmailContainer([
                de.EmailSection(
                    style={"backgroundColor": "#ffffff", "padding": "40px"},
                    children=[
                        de.EmailHeading("Title", as_="h1"),
                        de.EmailText("Content..."),
                        de.EmailButton("CTA", href="#")
                    ]
                )
            ])
        ]
    )
])
```

### Two-Column Layout

```python
de.EmailRow([
    de.EmailColumn(
        style={"width": "50%", "padding": "20px"},
        children=[
            de.EmailImage(src="product1.jpg", width="100%"),
            de.EmailHeading("Product 1", as_="h3"),
            de.EmailText("$29.99")
        ]
    ),
    de.EmailColumn(
        style={"width": "50%", "padding": "20px"},
        children=[
            de.EmailImage(src="product2.jpg", width="100%"),
            de.EmailHeading("Product 2", as_="h3"),
            de.EmailText("$39.99")
        ]
    )
])
```

### Header + Content + Footer

```python
de.Email([
    de.EmailBody([
        de.EmailContainer([
            # Header
            de.EmailSection(
                style={"backgroundColor": "#1a1a2e", "padding": "20px", "textAlign": "center"},
                children=[
                    de.EmailImage(src="logo-white.png", width=120, alt="Logo")
                ]
            ),

            # Main Content
            de.EmailSection(
                style={"backgroundColor": "#ffffff", "padding": "40px"},
                children=[
                    de.EmailHeading("Main Title", as_="h1"),
                    de.EmailText("Main content goes here...")
                ]
            ),

            # Footer
            de.EmailSection(
                style={"padding": "20px", "textAlign": "center"},
                children=[
                    de.EmailText(
                        "© 2026 Company Name. All rights reserved.",
                        style={"color": "#999999", "fontSize": "12px"}
                    ),
                    de.EmailLink("Unsubscribe", href="#", style={"color": "#999999"})
                ]
            )
        ])
    ])
])
```

### Card Grid (Product Showcase)

```python
def product_card(image, title, price, link):
    return de.EmailColumn(
        style={"width": "33.33%", "padding": "10px"},
        children=[
            de.EmailSection(
                style={
                    "backgroundColor": "#ffffff",
                    "borderRadius": "8px",
                    "padding": "16px",
                    "textAlign": "center"
                },
                children=[
                    de.EmailImage(src=image, width="100%", alt=title),
                    de.EmailHeading(title, as_="h4", style={"margin": "12px 0 8px"}),
                    de.EmailText(price, style={"color": "#007bff", "fontWeight": "bold"}),
                    de.EmailButton("Buy Now", href=link, style={...})
                ]
            )
        ]
    )

# Usage
de.EmailRow([
    product_card("prod1.jpg", "Product 1", "$29", "#"),
    product_card("prod2.jpg", "Product 2", "$39", "#"),
    product_card("prod3.jpg", "Product 3", "$49", "#"),
])
```

---

## AI-Powered Generation

### Using the Gemini Handler

The `utils/gemini_handler.py` module provides AI-powered email generation.

```python
from utils.gemini_handler import generate_email_content

result = generate_email_content(
    email_type="welcome",              # See email types below
    user_content="Welcome new users to our fitness app",
    image_urls=["https://example.com/hero.jpg"]  # Optional
)

# Result structure
{
    "subject": "Welcome to FitLife! Your Journey Starts Now",
    "full_code": "import dash_email as de\n\nemail = de.Email(...)",
    "preview_code": "de.Email(...)",
    "raw_response": "..."
}
```

### Supported Email Types

| Category | Types |
|----------|-------|
| **Marketing & Sales** | `promotional`, `welcome`, `abandoned_cart`, `re_engagement`, `lead_nurturing`, `newsletter` |
| **Transactional** | `order_confirmation`, `onboarding`, `feedback`, `announcement`, `milestone` |
| **Professional** | `personal`, `professional`, `follow_up`, `thank_you` |
| **Other** | `educational`, `invitation` |

### Generation Prompt Tips

**Good prompts:**
```
"Welcome email for a SaaS project management tool, emphasize free trial"
"Order confirmation for an e-commerce store selling electronics"
"Newsletter for a cooking blog featuring 3 recipes"
```

**Include specifics:**
- Brand name and industry
- Key message or CTA
- Tone (professional, casual, urgent)
- Any specific content to include

---

## Email Sending with Resend

### Basic Setup

```python
import os
from dotenv import load_dotenv
import resend

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")
```

### Sending a Single Email

```python
from utils.email_sender import send_email

result = send_email(
    to_email="recipient@example.com",
    subject="Your Order Confirmation",
    html_content="<html>...</html>",
    from_email="orders@yourdomain.com",  # Must be verified domain
    embed_images=True,                    # Convert images to CID
    scheduled_at=None,                    # Or ISO 8601 / natural language
    file_attachments=None                 # Or list of attachment dicts
)

# Result
{
    "success": True,
    "message": "Email sent! ID: abc123",
    "email_id": "abc123",
    "response": {...}
}
```

### Scheduling Emails

```python
# ISO 8601 format
result = send_email(
    to_email="user@example.com",
    subject="Reminder",
    html_content=html,
    scheduled_at="2026-01-15T09:00:00.000Z"
)

# Natural language (Resend parses these)
result = send_email(
    to_email="user@example.com",
    subject="Reminder",
    html_content=html,
    scheduled_at="tomorrow at 9am"
)

# Relative time
scheduled_at="in 2 hours"
scheduled_at="next monday at 10am"
```

**Constraints:**
- Maximum 30 days in advance
- Not available for batch sending

### Batch Sending

```python
from utils.email_sender import send_batch_emails

result = send_batch_emails(
    recipients=["user1@example.com", "user2@example.com", ...],
    subject="Newsletter",
    html_content=html,
    from_email="newsletter@yourdomain.com"
)

# Result
{
    "success": True,
    "total": 50,
    "data": {...}
}
```

**Constraints:**
- Maximum 100 recipients per batch
- No attachments supported
- No scheduling supported

### File Attachments

```python
import base64

# Read file and encode
with open("invoice.pdf", "rb") as f:
    content = base64.b64encode(f.read()).decode()

attachments = [
    {
        "content": content,
        "filename": "invoice.pdf"
    }
]

result = send_email(
    to_email="customer@example.com",
    subject="Your Invoice",
    html_content=html,
    file_attachments=attachments
)
```

---

## Template Management

### Creating Templates

```python
from utils.template_handler import create_template

result = create_template(
    name="Welcome Email v1",
    subject="Welcome to {{{COMPANY_NAME}}}!",
    html="<html>Hello {{{NAME}}}, welcome to {{{COMPANY_NAME}}}...</html>",
    from_email="hello@yourdomain.com",
    variables=[
        {"key": "NAME", "type": "string", "fallback_value": "Customer"},
        {"key": "COMPANY_NAME", "type": "string", "fallback_value": "Our Platform"}
    ]
)

# Result
{
    "success": True,
    "template_id": "tmpl_abc123",
    "message": "Template 'Welcome Email v1' created successfully!"
}
```

### Variable Syntax

Use triple curly braces in HTML:
```html
<p>Hello {{{NAME}}},</p>
<p>Your order total: ${{{TOTAL}}}</p>
<p>Track at: {{{TRACKING_URL}}}</p>
```

**Reserved Variable Names (cannot use):**
- `FIRST_NAME`, `LAST_NAME`, `EMAIL`
- `RESEND_UNSUBSCRIBE_URL`
- `contact`, `this`

### Sending with Templates

```python
from utils.template_handler import send_with_template

result = send_with_template(
    to_email="customer@example.com",
    template_id="tmpl_abc123",
    template_data={
        "NAME": "John",
        "COMPANY_NAME": "Acme Corp",
        "TOTAL": "99.99"
    },
    from_email="orders@yourdomain.com",
    scheduled_at=None
)
```

### Managing Templates

```python
from utils.template_handler import list_templates, get_template, delete_template

# List all templates
templates = list_templates()
# {"success": True, "templates": [...], "count": 5}

# Get specific template
template = get_template("tmpl_abc123")
# {"success": True, "template": {...}}

# Delete template
result = delete_template("tmpl_abc123")
# {"success": True, "message": "Template deleted..."}
```

---

## Image Handling

### Inline Image Embedding (CID)

The email sender automatically converts local images to CID attachments:

```python
# In your HTML
html = '''
<img src="/assets/uploads/logo.png" alt="Logo">
<img src="assets/hero.jpg" alt="Hero">
'''

# send_email with embed_images=True converts to:
# <img src="cid:abc123" alt="Logo">
# And attaches the image with Content-ID: abc123
```

**Benefits:**
- Images display even with "block images" enabled
- No external hosting required for logos/icons
- Faster loading

### Image Upload Handling

```python
from utils.image_handler import save_uploaded_image, save_multiple_images

# Single image (from Dash Upload component)
# contents = "data:image/png;base64,iVBORw0KGgo..."
result = save_uploaded_image(base64_data, "logo.png")
# {"success": True, "path": "/assets/uploads/abc123.png", "url": "/assets/uploads/abc123.png"}

# Multiple images
results = save_multiple_images(
    base64_images=["data:image/png;base64,...", "data:image/jpg;base64,..."],
    filenames=["image1.png", "image2.jpg"]
)
```

### Image Cleanup

```python
from utils.image_handler import cleanup_old_uploads, get_upload_stats

# Remove files older than 24 hours (default)
cleanup_old_uploads(max_age_hours=24)

# Get storage statistics
stats = get_upload_stats()
# {"count": 15, "total_bytes": 2500000, "oldest_age_hours": 12.5}
```

---

## Common Recipes

### Welcome Email

```python
def create_welcome_email(user_name, company_name):
    return de.Email([
        de.EmailPreview(f"Welcome to {company_name}!"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc"},
            children=[
                de.EmailContainer([
                    # Logo header
                    de.EmailSection(
                        style={"padding": "40px 20px", "textAlign": "center"},
                        children=[
                            de.EmailImage(src="logo.png", width=150, alt=company_name)
                        ]
                    ),
                    # Main content
                    de.EmailSection(
                        style={
                            "backgroundColor": "#ffffff",
                            "padding": "40px",
                            "borderRadius": "8px"
                        },
                        children=[
                            de.EmailHeading(f"Welcome, {user_name}!", as_="h1"),
                            de.EmailText(
                                "We're thrilled to have you join us. Here's what you can do next:"
                            ),
                            de.EmailButton(
                                "Get Started",
                                href="https://app.example.com/onboarding",
                                style={
                                    "backgroundColor": "#007bff",
                                    "color": "#ffffff",
                                    "padding": "14px 28px",
                                    "borderRadius": "6px",
                                    "marginTop": "20px"
                                }
                            )
                        ]
                    ),
                    # Footer
                    de.EmailSection(
                        style={"padding": "20px", "textAlign": "center"},
                        children=[
                            de.EmailText(
                                "Questions? Reply to this email.",
                                style={"color": "#999999", "fontSize": "14px"}
                            )
                        ]
                    )
                ])
            ]
        )
    ])
```

### Order Confirmation

```python
def create_order_email(order_id, items, total, shipping_address):
    item_rows = [
        de.EmailRow([
            de.EmailColumn(
                style={"width": "60%"},
                children=[de.EmailText(item["name"])]
            ),
            de.EmailColumn(
                style={"width": "20%", "textAlign": "center"},
                children=[de.EmailText(str(item["qty"]))]
            ),
            de.EmailColumn(
                style={"width": "20%", "textAlign": "right"},
                children=[de.EmailText(f"${item['price']:.2f}")]
            )
        ])
        for item in items
    ]

    return de.Email([
        de.EmailPreview(f"Order #{order_id} confirmed"),
        de.EmailBody([
            de.EmailContainer([
                de.EmailSection(
                    style={"backgroundColor": "#ffffff", "padding": "40px"},
                    children=[
                        de.EmailHeading("Order Confirmed!", as_="h1"),
                        de.EmailText(f"Order #{order_id}"),
                        de.EmailDivider(style={"margin": "24px 0"}),

                        # Items header
                        de.EmailRow([
                            de.EmailColumn(style={"width": "60%"}, children=[
                                de.EmailText("Item", style={"fontWeight": "bold"})
                            ]),
                            de.EmailColumn(style={"width": "20%", "textAlign": "center"}, children=[
                                de.EmailText("Qty", style={"fontWeight": "bold"})
                            ]),
                            de.EmailColumn(style={"width": "20%", "textAlign": "right"}, children=[
                                de.EmailText("Price", style={"fontWeight": "bold"})
                            ])
                        ]),

                        *item_rows,

                        de.EmailDivider(style={"margin": "24px 0"}),

                        # Total
                        de.EmailRow([
                            de.EmailColumn(style={"width": "60%"}, children=[]),
                            de.EmailColumn(style={"width": "40%", "textAlign": "right"}, children=[
                                de.EmailText(
                                    f"Total: ${total:.2f}",
                                    style={"fontWeight": "bold", "fontSize": "18px"}
                                )
                            ])
                        ]),

                        de.EmailButton(
                            "Track Order",
                            href=f"https://example.com/track/{order_id}",
                            style={
                                "backgroundColor": "#28a745",
                                "color": "#ffffff",
                                "padding": "14px 28px",
                                "marginTop": "24px"
                            }
                        )
                    ]
                )
            ])
        ])
    ])
```

### Newsletter with Multiple Sections

```python
def create_newsletter(articles, featured_products):
    article_sections = [
        de.EmailSection(
            style={"marginBottom": "32px"},
            children=[
                de.EmailHeading(article["title"], as_="h2"),
                de.EmailText(article["excerpt"]),
                de.EmailLink("Read more →", href=article["url"])
            ]
        )
        for article in articles
    ]

    product_cols = [
        de.EmailColumn(
            style={"width": f"{100//len(featured_products)}%", "padding": "10px"},
            children=[
                de.EmailImage(src=p["image"], width="100%", alt=p["name"]),
                de.EmailText(p["name"], style={"fontWeight": "bold"}),
                de.EmailText(p["price"])
            ]
        )
        for p in featured_products
    ]

    return de.Email([
        de.EmailBody([
            de.EmailContainer([
                # Header
                de.EmailSection(
                    style={"backgroundColor": "#1a1a2e", "padding": "30px", "textAlign": "center"},
                    children=[
                        de.EmailHeading(
                            "Weekly Newsletter",
                            as_="h1",
                            style={"color": "#ffffff", "margin": "0"}
                        )
                    ]
                ),

                # Articles
                de.EmailSection(
                    style={"backgroundColor": "#ffffff", "padding": "40px"},
                    children=[
                        de.EmailHeading("This Week's Articles", as_="h2"),
                        *article_sections
                    ]
                ),

                # Featured Products
                de.EmailSection(
                    style={"backgroundColor": "#f6f9fc", "padding": "40px"},
                    children=[
                        de.EmailHeading("Featured Products", as_="h2"),
                        de.EmailRow(product_cols)
                    ]
                ),

                # Footer
                de.EmailSection(
                    style={"padding": "20px", "textAlign": "center"},
                    children=[
                        de.EmailText(
                            "You received this because you subscribed to our newsletter.",
                            style={"color": "#999999", "fontSize": "12px"}
                        ),
                        de.EmailLink(
                            "Unsubscribe",
                            href="{{unsubscribe_url}}",
                            style={"color": "#999999", "fontSize": "12px"}
                        )
                    ]
                )
            ])
        ])
    ])
```

---

## Troubleshooting

### Common Issues

**1. Styles not applying**
```python
# ❌ Wrong - using kebab-case
style={"background-color": "#ffffff"}

# ✅ Correct - use camelCase
style={"backgroundColor": "#ffffff"}
```

**2. Layout breaking in Outlook**
```python
# ❌ Wrong - using divs for columns
html.Div([col1, col2], style={"display": "flex"})

# ✅ Correct - use EmailRow/EmailColumn
de.EmailRow([
    de.EmailColumn(col1_content),
    de.EmailColumn(col2_content)
])
```

**3. Images not displaying**
```python
# ❌ Wrong - relative path in production
de.EmailImage(src="/static/logo.png")

# ✅ Correct - absolute URL
de.EmailImage(src="https://cdn.example.com/logo.png")

# Or use CID embedding
send_email(..., embed_images=True)
```

**4. `as` keyword error**
```python
# ❌ Wrong - 'as' is Python reserved
de.EmailHeading("Title", as="h1")

# ✅ Correct - use 'as_' with underscore
de.EmailHeading("Title", as_="h1")
```

**5. Children formatting**
```python
# ❌ Wrong - string children for multiple items
de.EmailContainer("Item 1", "Item 2")

# ✅ Correct - use list for multiple children
de.EmailContainer([
    de.EmailText("Item 1"),
    de.EmailText("Item 2")
])

# ✅ Also correct - single child can be direct
de.EmailContainer(de.EmailText("Single item"))
```

### Email Client Specific Issues

**Gmail:**
- Strips `<style>` tags - use inline styles
- Clips emails over 102KB
- May hide images by default

**Outlook (Windows):**
- Uses Word rendering engine
- Ignores `border-radius`
- Problems with `background-image`
- Use tables for all layouts

**Apple Mail:**
- Generally good support
- Watch for dark mode inversions

**Yahoo Mail:**
- Strips some CSS
- Test thoroughly

---

## Best Practices

### Design

1. **Mobile-first approach** - Many emails read on phones
2. **Single column for mobile** - Avoid complex layouts
3. **Large tap targets** - Buttons at least 44x44px
4. **Clear hierarchy** - One primary CTA per email
5. **Preheader text** - Use EmailPreview for context

### Content

1. **Concise subject lines** - Under 50 characters
2. **Preview text matters** - First 100-150 characters shown in inbox
3. **Alt text for images** - Accessibility and blocked images
4. **Unsubscribe link** - Required by law (CAN-SPAM, GDPR)
5. **Plain text fallback** - Consider for accessibility

### Technical

1. **Test across clients** - Use Litmus or Email on Acid
2. **Keep under 102KB** - Gmail clips larger emails
3. **Optimize images** - Compress, use appropriate formats
4. **Use absolute URLs** - For images and links
5. **Validate HTML** - Check for unclosed tags

### Performance

1. **Compress images** - Use TinyPNG or similar
2. **Limit image count** - Each adds to load time
3. **Avoid video** - Use GIFs or static images with play button
4. **Web fonts optional** - Use sparingly, always have fallback

---

## Quick Reference

### Import Statement
```python
import dash_email as de
```

### Component Hierarchy
```
Email
├── EmailHead
│   └── EmailFont
├── EmailPreview
└── EmailBody
    └── EmailContainer
        └── EmailSection
            ├── EmailHeading
            ├── EmailText
            ├── EmailImage
            ├── EmailButton
            ├── EmailLink
            ├── EmailDivider
            └── EmailRow
                └── EmailColumn
```

### Style Property Cheatsheet
```python
{
    # Colors
    "color": "#333",
    "backgroundColor": "#fff",

    # Typography
    "fontSize": "16px",
    "fontWeight": "bold",
    "lineHeight": "1.6",
    "textAlign": "center",

    # Spacing
    "padding": "20px",
    "margin": "10px 0",

    # Borders
    "border": "1px solid #eee",
    "borderRadius": "8px",

    # Dimensions
    "width": "100%",
    "maxWidth": "600px",
}
```

### Environment Variables
```bash
RESEND_API_KEY=re_xxx          # Required for sending
GOOGLE_API_KEY=xxx             # Required for AI generation
LOGGER_MODE=debug|tail|none    # Logging verbosity
```

---

*Last updated: January 2026*
