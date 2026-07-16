# Dash Email - Project Status Reference

**Version:** 0.0.1
**Last Updated:** January 2026
**Status:** Ready for PyPI Release

---

## Project Overview

**dash-email** is a Plotly Dash component library that wraps React Email components, enabling Python developers to build, preview, and send professional email templates directly within Dash applications.

---

## Directory Structure

```
dash-email/
├── src/lib/components/          # React components (15 total)
│   ├── Email.react.js           # Root email wrapper
│   ├── EmailBody.react.js       # Body container
│   ├── EmailButton.react.js     # CTA button
│   ├── EmailColumn.react.js     # Table column
│   ├── EmailContainer.react.js  # Centered container (600px max)
│   ├── EmailDivider.react.js    # Horizontal divider
│   ├── EmailFont.react.js       # Custom font loading
│   ├── EmailHead.react.js       # Email metadata
│   ├── EmailHeading.react.js    # h1-h6 headings
│   ├── EmailImage.react.js      # Image element
│   ├── EmailLink.react.js       # Hyperlink
│   ├── EmailPreview.react.js    # Inbox preview text
│   ├── EmailRow.react.js        # Table row
│   ├── EmailSection.react.js    # Content grouping
│   ├── EmailText.react.js       # Paragraph text
│   └── index.js                 # Component exports
│
├── dash_email/                  # Auto-generated Python package
│   ├── __init__.py
│   ├── *.py                     # Python component wrappers
│   ├── dash_email.min.js        # Bundled React components
│   └── metadata.json
│
├── pages/                       # Dash pages
│   ├── home.py                  # Landing page
│   └── email_builder.py         # Main builder interface
│
├── utils/                       # Utility modules
│   ├── gemini_handler.py        # Google Gemini AI integration
│   ├── email_sender.py          # Resend email sending
│   ├── template_handler.py      # Resend template management
│   ├── image_handler.py         # Image upload handling
│   └── wide_event_logger.py     # Structured event logging
│
├── app.py                       # Main Dash application
├── usage.py                     # Example usage
├── setup.py                     # Package installation
├── requirements.txt             # Python dependencies
├── package.json                 # npm dependencies
└── webpack.config.js            # Build configuration
```

---

## Components Reference

| Component | Description | Key Props |
|-----------|-------------|-----------|
| `Email` | Root wrapper for email templates | `lang`, `dir`, `style` |
| `EmailHead` | Email metadata section | `children` |
| `EmailPreview` | Inbox preview text (hidden in body) | `children` |
| `EmailBody` | Main body wrapper | `style`, `children` |
| `EmailContainer` | Centered container (600px max-width) | `style`, `children` |
| `EmailSection` | Content grouping | `style`, `children` |
| `EmailRow` | Horizontal row (table-based) | `style`, `children` |
| `EmailColumn` | Column within row | `style`, `children` |
| `EmailHeading` | Heading text (h1-h6) | `as_`, `style`, `children` |
| `EmailText` | Paragraph text | `style`, `children` |
| `EmailButton` | Styled link button | `href`, `target`, `style` |
| `EmailLink` | Hyperlink | `href`, `target`, `style` |
| `EmailImage` | Image element | `src`, `alt`, `width`, `height` |
| `EmailDivider` | Horizontal divider | `style` |
| `EmailFont` | Custom font loading | `fontFamily`, `fallbackFontFamily`, `webFont` |

---

## Features Implemented

### 1. Email Builder Interface (`pages/email_builder.py`)

**Left Panel - Controls:**
- Email type selection (16 types across 4 categories)
- Requirements text input
- Image upload with drag-and-drop
- Generate button with loading state

**Right Panel - Tabs:**
- **Preview**: Live email rendering
- **Code**: Syntax-highlighted Python source
- **Send**: Single, batch, schedule, templates

### 2. AI-Powered Generation (`utils/gemini_handler.py`)

- Google Gemini 2.5-Flash model
- 16+ email type support
- Image context understanding
- Python code generation with validation

**Email Types:**
| Marketing & Sales | Transactional | Professional | Other |
|-------------------|---------------|--------------|-------|
| Promotional | Order Confirmation | Personal | Educational |
| Welcome | Onboarding | Professional | Invitation |
| Abandoned Cart | Feedback Request | Follow-Up | |
| Re-engagement | Announcement | Thank You | |
| Lead Nurturing | Milestone | | |
| Newsletter | | | |

### 3. Email Sending (`utils/email_sender.py`)

- **Single Send**: Individual emails with attachments
- **Batch Send**: Up to 100 recipients
- **Scheduling**: Up to 30 days in advance
- **Inline Images**: CID attachment embedding
- **File Attachments**: Base64 encoded files

### 4. Template Management (`utils/template_handler.py`)

- Create, list, get, delete templates
- Send with template variables
- Variable syntax: `{{{VARIABLE_NAME}}}`

### 5. Image Handling (`utils/image_handler.py`)

- Base64 to disk conversion
- UUID-based filenames
- Auto-cleanup (24-hour retention)
- Supports: PNG, JPG, GIF, WebP, SVG

### 6. Event Logging (`utils/wide_event_logger.py`)

- Wide Events pattern
- Three modes: DEBUG, TAIL, NONE
- Tracks: AI generation, email sending, templates, images

---

## API Integrations

### Google Gemini AI
- **Model:** gemini-2.5-flash
- **Env Var:** `GOOGLE_API_KEY` or `GEMINI_API_KEY`
- **Purpose:** Email template generation

### Resend Email Service
- **Env Var:** `RESEND_API_KEY`
- **Features:** Send, batch, schedule, templates

---

## Dependencies

### Python (`requirements.txt`)
```
dash>=3.0.0
dash-mantine-components>=2.4.0
dash-iconify>=0.1.2
google-genai>=1.0.0
resend>=2.0.0
python-dotenv>=1.0.0
pandas>=2.0.0
```

### JavaScript (`package.json`)
```json
{
  "dependencies": {
    "@react-email/components": "^0.0.31",
    "ramda": "^0.29.0"
  },
  "peerDependencies": {
    "react": ">=18.0.0",
    "react-dom": ">=18.0.0"
  }
}
```

---

## Build Commands

```bash
# Install dependencies
npm install
pip install -e .

# Build for production
npm run build

# Development build with watch
npm run build:dev:watch

# Extract component metadata
npm run extract-meta

# Run tests
pytest tests/
```

---

## Environment Configuration

Create a `.env` file:
```bash
RESEND_API_KEY=re_your_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
LOGGER_MODE=debug  # debug|tail|none
```

---

## Technical Decisions

### Dash 3.0 Compatibility
- All components use JavaScript default parameters instead of `defaultProps`
- Eliminates React 18.3 deprecation warnings

### Email Client Compatibility
- Table-based layouts (`EmailRow` uses `<table>`)
- 600px max-width container (industry standard)
- Inline styles only (no external CSS)

### Code Generation
- Enforces camelCase for style properties
- Uses `as_` instead of `as` (Python reserved keyword)
- Validates syntax before returning

---

## Metrics

| File | Lines | Description |
|------|-------|-------------|
| `pages/email_builder.py` | ~1200 | Main builder interface |
| `utils/email_sender.py` | ~400 | Email sending logic |
| `utils/gemini_handler.py` | ~290 | AI integration |
| `utils/wide_event_logger.py` | ~400 | Logging system |
| `utils/template_handler.py` | ~300 | Template management |
| `utils/image_handler.py` | ~250 | Image handling |

---

## Known Limitations

1. **Batch Sending**: No attachments or scheduling support
2. **Templates**: Cannot use reserved variable names (FIRST_NAME, LAST_NAME, EMAIL)
3. **Scheduling**: Maximum 30 days in advance
4. **Images**: Local images require base URL configuration for external access

---

## Next Steps for PyPI Release

1. [x] Convert all `defaultProps` to default parameters
2. [x] Rebuild component library
3. [ ] Update `setup.py` with accurate metadata
4. [ ] Create PyPI account if needed
5. [ ] Build distribution packages
6. [ ] Upload to PyPI

---

## Usage Example

```python
import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview("Welcome to our platform!"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc"},
            children=[
                de.EmailContainer([
                    de.EmailSection(
                        style={
                            "backgroundColor": "#ffffff",
                            "borderRadius": "8px",
                            "padding": "40px"
                        },
                        children=[
                            de.EmailHeading("Welcome!", as_="h1"),
                            de.EmailText("Thanks for signing up."),
                            de.EmailButton(
                                "Get Started",
                                href="https://example.com",
                                style={
                                    "backgroundColor": "#007bff",
                                    "color": "#ffffff",
                                    "padding": "12px 24px",
                                    "borderRadius": "4px"
                                }
                            )
                        ]
                    )
                ])
            ]
        )
    ]
)
```
