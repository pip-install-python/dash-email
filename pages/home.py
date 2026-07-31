"""
Home page - Landing page for Dash Email
"""
import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from lib.constants import PAGE_TITLE_PREFIX

dash.register_page(__name__, path="/", name="Home", title=PAGE_TITLE_PREFIX + "Home")

# Served verbatim at /llms.txt by dash-improve-my-llms.
LLMS_DOC = """# Dash Email

A Plotly Dash component library wrapping React Email patterns. 15 email-safe
components (Email, EmailBody, EmailContainer, EmailSection, EmailRow,
EmailColumn, EmailHeading, EmailText, EmailButton, EmailLink, EmailImage,
EmailDivider, EmailFont, EmailHead, EmailPreview) for building, previewing,
and sending HTML emails from Python.

- Install: `pip install dash-email`
- Docs: /getting-started and the /components/* pages (each serves /<page>/llms.txt)
- App: /email-builder — AI-powered template builder (Google Gemini) with live
  preview, Python code export, and sending via Resend.
- Source: https://github.com/pip-install-python/dash-email
"""

# Feature cards data
features = [
    {
        "icon": "tabler:sparkles",
        "title": "AI-Powered Generation",
        "description": "Use Google Gemini AI to generate professional email templates based on your requirements."
    },
    {
        "icon": "tabler:mail",
        "title": "Multiple Email Types",
        "description": "Support for marketing, transactional, professional, and many other email categories."
    },
    {
        "icon": "tabler:photo",
        "title": "Image Support",
        "description": "Upload and include images in your email templates with AI understanding."
    },
    {
        "icon": "tabler:code",
        "title": "Code Export",
        "description": "Get ready-to-use Python code with dash_email components for your Dash apps."
    },
    {
        "icon": "tabler:send",
        "title": "Send Emails",
        "description": "Test your emails by sending them directly via Resend integration."
    },
    {
        "icon": "tabler:eye",
        "title": "Live Preview",
        "description": "See your email template rendered in real-time as you build it."
    },
]


def create_feature_card(feature):
    """Create a feature card component."""
    return dmc.Card(
        children=[
            dmc.ThemeIcon(
                DashIconify(icon=feature["icon"], width=24),
                size=50,
                radius="md",
                variant="light",
                color="blue",
            ),
            dmc.Text(feature["title"], fw=500, size="lg", mt="md"),
            dmc.Text(feature["description"], size="sm", c="dimmed", mt="xs"),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        p="lg",
    )


def create_video_embed():
    """The demo video, in a 16:9 box that scales with the container.

    `youtube-nocookie.com` is the privacy-preserving host: it serves the same
    player but sets no tracking cookie until the viewer actually presses play,
    which keeps a documentation page from needing a consent banner.

    The shape is held by `aspectRatio` on the wrapper, with the iframe at
    100% x 100% inside it — not a fixed pixel height, which would letterbox on
    phones and crop on wide screens. `maxWidth` keeps it from ballooning past
    the text column on a desktop.
    """
    return dmc.Stack(
        align="center",
        gap="md",
        mb=50,
        children=[
            dmc.Title("See it in action", order=2, ta="center"),
            dmc.Text(
                "Build, preview and send emails inside your Dash app.",
                ta="center",
                c="dimmed",
            ),
            dmc.Paper(
                withBorder=True,
                radius="md",
                shadow="sm",
                p=0,
                style={
                    "width": "100%",
                    "maxWidth": 860,
                    "aspectRatio": "16 / 9",
                    "overflow": "hidden",
                },
                children=html.Iframe(
                    src="https://www.youtube-nocookie.com/embed/_30EHZ1-2vs",
                    title="Dash Email: Build, Preview & Send Emails Inside Your Dash App",
                    style={
                        "width": "100%",
                        "height": "100%",
                        "border": "none",
                        "display": "block",
                    },
                    # `fullscreen` rides in `allow` rather than as a separate
                    # `allowfullscreen` attribute: Dash's html.Iframe exposes
                    # no such prop (nor `loading`) and raises TypeError on
                    # unknown kwargs. The Permissions-Policy token is the
                    # modern equivalent and is what makes the player's
                    # fullscreen button work instead of sitting there inert.
                    allow=(
                        "accelerometer; autoplay; clipboard-write; "
                        "encrypted-media; gyroscope; picture-in-picture; "
                        "web-share; fullscreen"
                    ),
                    referrerPolicy="strict-origin-when-cross-origin",
                ),
            ),
        ],
    )


layout = dmc.Container(
    size="lg",
    py="xl",
    children=[
        # Hero Section
        dmc.Stack(
            align="center",
            gap="lg",
            mb=50,
            children=[
                dmc.ThemeIcon(
                    DashIconify(icon="tabler:mail-code", width=60),
                    size=100,
                    radius="xl",
                    variant="light",
                    color="blue",
                ),
                dmc.Title(
                    "Build Beautiful Emails with AI",
                    order=1,
                    ta="center",
                ),
                dmc.Text(
                    "Create professional email templates using AI-powered generation. "
                    "Design, preview, and export email templates as Dash components.",
                    ta="center",
                    size="lg",
                    c="dimmed",
                    maw=600,
                ),
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Button(
                                "Get Started",
                                size="lg",
                                leftSection=DashIconify(icon="tabler:rocket", width=20),
                            ),
                            href="/email-builder",
                        ),
                        dmc.Anchor(
                            dmc.Button(
                                "View Documentation",
                                size="lg",
                                variant="outline",
                                leftSection=DashIconify(icon="tabler:book", width=20),
                            ),
                            href="/getting-started",
                        ),
                    ],
                    gap="md",
                ),
            ],
        ),

        # Video Section
        create_video_embed(),

        # Features Section
        dmc.Title("Features", order=2, ta="center", mb="lg"),
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 2, "lg": 3},
            spacing="lg",
            children=[create_feature_card(f) for f in features],
        ),

        # Email Types Section
        dmc.Paper(
            mt=50,
            p="xl",
            radius="md",
            withBorder=True,
            children=[
                dmc.Title("Supported Email Types", order=3, mb="md"),
                dmc.SimpleGrid(
                    cols={"base": 1, "sm": 2, "lg": 4},
                    spacing="md",
                    children=[
                        dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Text("Marketing & Sales", fw=600, c="blue"),
                                dmc.List(
                                    size="sm",
                                    children=[
                                        dmc.ListItem("Promotional Emails"),
                                        dmc.ListItem("Welcome Emails"),
                                        dmc.ListItem("Abandoned Cart"),
                                        dmc.ListItem("Re-engagement"),
                                        dmc.ListItem("Lead Nurturing"),
                                        dmc.ListItem("Newsletters"),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Text("Transactional", fw=600, c="green"),
                                dmc.List(
                                    size="sm",
                                    children=[
                                        dmc.ListItem("Order Confirmations"),
                                        dmc.ListItem("Onboarding"),
                                        dmc.ListItem("Feedback/Survey"),
                                        dmc.ListItem("Announcements"),
                                        dmc.ListItem("Milestones"),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Text("Professional", fw=600, c="violet"),
                                dmc.List(
                                    size="sm",
                                    children=[
                                        dmc.ListItem("Personal Emails"),
                                        dmc.ListItem("Professional"),
                                        dmc.ListItem("Follow-Up"),
                                        dmc.ListItem("Thank You"),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Text("Other Types", fw=600, c="orange"),
                                dmc.List(
                                    size="sm",
                                    children=[
                                        dmc.ListItem("Educational"),
                                        dmc.ListItem("Invitations"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # Tech Stack
        dmc.Paper(
            mt=30,
            p="xl",
            radius="md",
            withBorder=True,
            children=[
                dmc.Title("Built With", order=3, mb="md"),
                dmc.Group(
                    gap="xl",
                    justify="center",
                    children=[
                        dmc.Stack(
                            align="center",
                            gap="xs",
                            children=[
                                DashIconify(icon="simple-icons:plotly", width=40, color="#3F4F75"),
                                dmc.Text("Dash", size="sm"),
                            ],
                        ),
                        dmc.Stack(
                            align="center",
                            gap="xs",
                            children=[
                                DashIconify(icon="simple-icons:react", width=40, color="#61DAFB"),
                                dmc.Text("React Email", size="sm"),
                            ],
                        ),
                        dmc.Stack(
                            align="center",
                            gap="xs",
                            children=[
                                DashIconify(icon="simple-icons:google", width=40, color="#4285F4"),
                                dmc.Text("Gemini AI", size="sm"),
                            ],
                        ),
                        dmc.Stack(
                            align="center",
                            gap="xs",
                            children=[
                                DashIconify(icon="tabler:send", width=40, color="#000000"),
                                dmc.Text("Resend", size="sm"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)