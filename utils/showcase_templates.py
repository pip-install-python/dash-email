"""
Curated example templates for the Email Builder.

These power the builder when no Gemini API key is configured: instead of
generating a template with AI, the builder serves a handcrafted one for the
selected email type. They return the same shape as gemini_handler's
generate_email_content(), so the page renders them through the same path.

Each entry is real dash_email source, so the code shown to the user is
copy-pasteable and doubles as documentation.
"""

_WELCOME = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="Welcome to TaskFlow — let's get you started"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, Arial, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px", "maxWidth": "600px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px",
                            },
                            children=[
                                de.EmailHeading(
                                    children="Welcome aboard!",
                                    as_="h1",
                                    style={"color": "#1a1a2e", "fontSize": "28px", "margin": "0 0 16px 0"},
                                ),
                                de.EmailText(
                                    children="Thanks for signing up for TaskFlow. Your account is ready, and you can start organizing your work right away.",
                                    style={"color": "#525f7f", "fontSize": "16px", "lineHeight": "24px"},
                                ),
                                de.EmailText(
                                    children="Your 14-day free trial has started.",
                                    style={"color": "#28a745", "fontSize": "16px", "fontWeight": "bold"},
                                ),
                                de.EmailButton(
                                    children="Start your first project",
                                    href="https://example.com/start",
                                    style={
                                        "backgroundColor": "#228be6",
                                        "color": "#ffffff",
                                        "padding": "12px 24px",
                                        "borderRadius": "6px",
                                        "textDecoration": "none",
                                        "fontWeight": "bold",
                                        "display": "inline-block",
                                        "margin": "16px 0",
                                    },
                                ),
                                de.EmailDivider(style={"borderColor": "#e6ebf1", "margin": "24px 0"}),
                                de.EmailText(
                                    children="Questions? Just reply to this email — a real person reads every one.",
                                    style={"color": "#8898aa", "fontSize": "14px"},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
'''

_PROMOTIONAL = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="48 hours only — 30% off everything"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, Arial, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px", "maxWidth": "600px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#1a1a2e",
                                "borderRadius": "8px 8px 0 0",
                                "padding": "40px",
                                "textAlign": "center",
                            },
                            children=[
                                de.EmailHeading(
                                    children="Spring Sale",
                                    as_="h1",
                                    style={"color": "#ffffff", "fontSize": "32px", "margin": "0"},
                                ),
                                de.EmailText(
                                    children="30% OFF",
                                    style={"color": "#ffd43b", "fontSize": "48px", "fontWeight": "bold", "margin": "8px 0"},
                                ),
                                de.EmailText(
                                    children="48 hours only",
                                    style={"color": "#dee2e6", "fontSize": "16px", "margin": "0"},
                                ),
                            ],
                        ),
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "0 0 8px 8px",
                                "padding": "40px",
                                "textAlign": "center",
                            },
                            children=[
                                de.EmailText(
                                    children="Use code SPRING30 at checkout. Applies to every item, including new arrivals.",
                                    style={"color": "#525f7f", "fontSize": "16px", "lineHeight": "24px"},
                                ),
                                de.EmailButton(
                                    children="Shop the sale",
                                    href="https://example.com/sale",
                                    style={
                                        "backgroundColor": "#fa5252",
                                        "color": "#ffffff",
                                        "padding": "14px 32px",
                                        "borderRadius": "6px",
                                        "textDecoration": "none",
                                        "fontWeight": "bold",
                                        "display": "inline-block",
                                        "margin": "16px 0",
                                    },
                                ),
                                de.EmailText(
                                    children="Ends Sunday at midnight.",
                                    style={"color": "#8898aa", "fontSize": "13px"},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
'''

_NEWSLETTER = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="This week: three stories worth your time"),
        de.EmailBody(
            style={"backgroundColor": "#f0f0f0", "fontFamily": "Inter, Arial, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "24px 20px", "maxWidth": "600px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#1a1a2e",
                                "padding": "30px",
                                "textAlign": "center",
                                "borderRadius": "8px 8px 0 0",
                            },
                            children=[
                                de.EmailHeading(
                                    children="The Weekly",
                                    as_="h1",
                                    style={"color": "#ffffff", "margin": "0", "fontSize": "26px"},
                                ),
                                de.EmailText(
                                    children="Issue #42",
                                    style={"color": "#adb5bd", "fontSize": "14px", "margin": "4px 0 0 0"},
                                ),
                            ],
                        ),
                        de.EmailSection(
                            style={"backgroundColor": "#ffffff", "padding": "32px"},
                            children=[
                                de.EmailHeading(
                                    children="Shipping faster with smaller PRs",
                                    as_="h2",
                                    style={"color": "#1a1a2e", "fontSize": "20px", "margin": "0 0 8px 0"},
                                ),
                                de.EmailText(
                                    children="Teams that keep pull requests under 200 lines merge nearly twice as fast. Here's how to split work without losing context.",
                                    style={"color": "#525f7f", "fontSize": "15px", "lineHeight": "23px"},
                                ),
                                de.EmailLink(
                                    children="Read the full story →",
                                    href="https://example.com/story-1",
                                    style={"color": "#228be6", "fontSize": "15px", "fontWeight": "bold"},
                                ),
                                de.EmailDivider(style={"borderColor": "#e6ebf1", "margin": "24px 0"}),
                                de.EmailHeading(
                                    children="A field guide to flaky tests",
                                    as_="h2",
                                    style={"color": "#1a1a2e", "fontSize": "20px", "margin": "0 0 8px 0"},
                                ),
                                de.EmailText(
                                    children="Most flakiness comes from four patterns. Learn to spot them before they reach your CI.",
                                    style={"color": "#525f7f", "fontSize": "15px", "lineHeight": "23px"},
                                ),
                                de.EmailLink(
                                    children="Read the full story →",
                                    href="https://example.com/story-2",
                                    style={"color": "#228be6", "fontSize": "15px", "fontWeight": "bold"},
                                ),
                            ],
                        ),
                        de.EmailSection(
                            style={
                                "backgroundColor": "#f8f9fa",
                                "padding": "20px",
                                "textAlign": "center",
                                "borderRadius": "0 0 8px 8px",
                            },
                            children=[
                                de.EmailText(
                                    children="You're receiving this because you subscribed to The Weekly.",
                                    style={"color": "#8898aa", "fontSize": "12px", "margin": "0"},
                                ),
                                de.EmailLink(
                                    children="Unsubscribe",
                                    href="https://example.com/unsubscribe",
                                    style={"color": "#8898aa", "fontSize": "12px", "textDecoration": "underline"},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
'''

_TRANSACTIONAL = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="Order #10432 confirmed — arriving Thursday"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, Arial, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px", "maxWidth": "600px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px",
                            },
                            children=[
                                de.EmailHeading(
                                    children="Order confirmed",
                                    as_="h1",
                                    style={"color": "#1a1a2e", "fontSize": "26px", "margin": "0 0 8px 0"},
                                ),
                                de.EmailText(
                                    children="Order #10432 · Placed March 14",
                                    style={"color": "#8898aa", "fontSize": "14px", "margin": "0 0 24px 0"},
                                ),
                                de.EmailRow(
                                    children=[
                                        de.EmailColumn(
                                            children=[
                                                de.EmailText(
                                                    children="Mechanical Keyboard",
                                                    style={"color": "#1a1a2e", "fontSize": "15px", "fontWeight": "bold", "margin": "0"},
                                                ),
                                                de.EmailText(
                                                    children="Qty 1",
                                                    style={"color": "#8898aa", "fontSize": "13px", "margin": "0"},
                                                ),
                                            ],
                                        ),
                                        de.EmailColumn(
                                            style={"textAlign": "right"},
                                            children=[
                                                de.EmailText(
                                                    children="$149.00",
                                                    style={"color": "#1a1a2e", "fontSize": "15px", "margin": "0"},
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                de.EmailDivider(style={"borderColor": "#e6ebf1", "margin": "16px 0"}),
                                de.EmailRow(
                                    children=[
                                        de.EmailColumn(
                                            children=[
                                                de.EmailText(
                                                    children="Total",
                                                    style={"color": "#1a1a2e", "fontSize": "16px", "fontWeight": "bold", "margin": "0"},
                                                ),
                                            ],
                                        ),
                                        de.EmailColumn(
                                            style={"textAlign": "right"},
                                            children=[
                                                de.EmailText(
                                                    children="$149.00",
                                                    style={"color": "#1a1a2e", "fontSize": "16px", "fontWeight": "bold", "margin": "0"},
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                de.EmailText(
                                    children="Estimated delivery: Thursday, March 20",
                                    style={"color": "#28a745", "fontSize": "15px", "fontWeight": "bold", "margin": "24px 0 0 0"},
                                ),
                                de.EmailButton(
                                    children="Track your order",
                                    href="https://example.com/track/10432",
                                    style={
                                        "backgroundColor": "#1a1a2e",
                                        "color": "#ffffff",
                                        "padding": "12px 24px",
                                        "borderRadius": "6px",
                                        "textDecoration": "none",
                                        "fontWeight": "bold",
                                        "display": "inline-block",
                                        "margin": "16px 0 0 0",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
'''

_ANNOUNCEMENT = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="Introducing scheduled sends"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, Arial, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px", "maxWidth": "600px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px",
                            },
                            children=[
                                de.EmailText(
                                    children="PRODUCT UPDATE",
                                    style={"color": "#228be6", "fontSize": "12px", "fontWeight": "bold", "letterSpacing": "1px", "margin": "0 0 8px 0"},
                                ),
                                de.EmailHeading(
                                    children="Scheduled sends are here",
                                    as_="h1",
                                    style={"color": "#1a1a2e", "fontSize": "28px", "margin": "0 0 16px 0"},
                                ),
                                de.EmailText(
                                    children="You can now pick the exact moment an email goes out — down to the minute, in your recipient's timezone. No more staying up to hit send.",
                                    style={"color": "#525f7f", "fontSize": "16px", "lineHeight": "24px"},
                                ),
                                de.EmailText(
                                    children="Available on every plan, starting today.",
                                    style={"color": "#525f7f", "fontSize": "16px", "lineHeight": "24px"},
                                ),
                                de.EmailButton(
                                    children="See what's new",
                                    href="https://example.com/changelog",
                                    style={
                                        "backgroundColor": "#228be6",
                                        "color": "#ffffff",
                                        "padding": "12px 24px",
                                        "borderRadius": "6px",
                                        "textDecoration": "none",
                                        "fontWeight": "bold",
                                        "display": "inline-block",
                                        "margin": "16px 0 0 0",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
'''

_THANK_YOU = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="Thank you for speaking at DashCon"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, Arial, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px", "maxWidth": "600px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px",
                            },
                            children=[
                                de.EmailHeading(
                                    children="Thank you, truly",
                                    as_="h1",
                                    style={"color": "#1a1a2e", "fontSize": "26px", "margin": "0 0 16px 0"},
                                ),
                                de.EmailText(
                                    children="Your talk on building accessible dashboards was the highest-rated session of the day. Several attendees told us it changed how they think about color contrast.",
                                    style={"color": "#525f7f", "fontSize": "16px", "lineHeight": "24px"},
                                ),
                                de.EmailText(
                                    children="We've attached your speaker feedback summary, and we'd love to have you back next year.",
                                    style={"color": "#525f7f", "fontSize": "16px", "lineHeight": "24px"},
                                ),
                                de.EmailDivider(style={"borderColor": "#e6ebf1", "margin": "24px 0"}),
                                de.EmailText(
                                    children="— The DashCon team",
                                    style={"color": "#8898aa", "fontSize": "14px", "fontStyle": "italic"},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
'''

_INVITATION = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview(children="You're invited: Building Better Emails, April 9"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, Arial, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px", "maxWidth": "600px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px",
                                "textAlign": "center",
                            },
                            children=[
                                de.EmailText(
                                    children="YOU'RE INVITED",
                                    style={"color": "#7950f2", "fontSize": "12px", "fontWeight": "bold", "letterSpacing": "2px", "margin": "0 0 12px 0"},
                                ),
                                de.EmailHeading(
                                    children="Building Better Emails",
                                    as_="h1",
                                    style={"color": "#1a1a2e", "fontSize": "28px", "margin": "0 0 8px 0"},
                                ),
                                de.EmailText(
                                    children="A free 45-minute webinar",
                                    style={"color": "#8898aa", "fontSize": "16px", "margin": "0 0 24px 0"},
                                ),
                                de.EmailDivider(style={"borderColor": "#e6ebf1", "margin": "0 0 24px 0"}),
                                de.EmailText(
                                    children="Thursday, April 9 · 2:00 PM ET",
                                    style={"color": "#1a1a2e", "fontSize": "17px", "fontWeight": "bold", "margin": "0 0 8px 0"},
                                ),
                                de.EmailText(
                                    children="We'll cover table-based layouts, dark-mode quirks, and why Outlook still needs special care.",
                                    style={"color": "#525f7f", "fontSize": "15px", "lineHeight": "23px"},
                                ),
                                de.EmailButton(
                                    children="Save my seat",
                                    href="https://example.com/webinar",
                                    style={
                                        "backgroundColor": "#7950f2",
                                        "color": "#ffffff",
                                        "padding": "14px 32px",
                                        "borderRadius": "6px",
                                        "textDecoration": "none",
                                        "fontWeight": "bold",
                                        "display": "inline-block",
                                        "margin": "16px 0 0 0",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
'''

# email_type -> curated example. Keys match the chip values in EMAIL_CATEGORIES.
SHOWCASE_TEMPLATES = {
    "welcome": {
        "subject": "Welcome to TaskFlow — your trial starts now",
        "full_code": _WELCOME,
    },
    "promotional": {
        "subject": "48 hours only: 30% off everything",
        "full_code": _PROMOTIONAL,
    },
    "newsletter": {
        "subject": "The Weekly #42: three stories worth your time",
        "full_code": _NEWSLETTER,
    },
    "transactional": {
        "subject": "Your order #10432 is confirmed",
        "full_code": _TRANSACTIONAL,
    },
    "announcement": {
        "subject": "New: schedule your sends down to the minute",
        "full_code": _ANNOUNCEMENT,
    },
    "thank_you": {
        "subject": "Thank you for speaking at DashCon",
        "full_code": _THANK_YOU,
    },
    "invitation": {
        "subject": "You're invited: Building Better Emails, April 9",
        "full_code": _INVITATION,
    },
}

SHOWCASE_TYPES = frozenset(SHOWCASE_TEMPLATES)


def has_showcase(email_type: str) -> bool:
    """True when a curated example exists for this email type."""
    return _normalize(email_type) in SHOWCASE_TEMPLATES


def _normalize(email_type: str) -> str:
    return (email_type or "").lower().replace(" ", "_").replace("-", "_")


def _to_preview_code(full_code: str) -> str:
    """
    Reduce a full template to the bare de.Email(...) expression.

    The builder's create_preview_from_code() evaluates a single expression, so
    strip the import and the `email = ` binding.
    """
    lines = [
        line for line in full_code.split("\n")
        if not line.strip().startswith("import")
    ]
    code = "\n".join(lines).strip()
    if code.startswith("email = "):
        code = code[len("email = "):]
    return code.strip()


def get_showcase_template(email_type: str) -> dict:
    """
    Return a curated template in the same shape as generate_email_content().

    Returns a dict with an "error" key when no example exists for the type,
    matching how the AI path signals failure.
    """
    template = SHOWCASE_TEMPLATES.get(_normalize(email_type))
    if template is None:
        available = ", ".join(sorted(SHOWCASE_TEMPLATES))
        message = (
            f"No example template for '{email_type}'. Examples are available "
            f"for: {available}. Set GOOGLE_API_KEY to generate any type with AI."
        )
        return {
            "subject": "",
            "full_code": f"# {message}",
            "preview_code": "",
            "raw_response": message,
            "error": message,
        }

    full_code = template["full_code"]
    return {
        "subject": template["subject"],
        "full_code": full_code,
        "preview_code": _to_preview_code(full_code),
        "raw_response": "",
        "showcase": True,
    }
