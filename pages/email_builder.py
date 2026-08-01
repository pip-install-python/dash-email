"""
Email Builder Page - Main interface for creating emails with AI
"""
import dash
import io
import base64
import uuid
from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_email as de
from lib.constants import OG_IMAGE_URL, PAGE_TITLE_PREFIX
from utils.ai_config import is_ai_enabled
from utils.image_handler import save_multiple_images, cleanup_old_uploads
from utils.showcase_templates import SHOWCASE_TYPES

# `description=`, `title=` and `image_url=` are load-bearing, not decoration:
# Dash emits `description`, `og:description`, `og:image` and `twitter:image`
# for every page from this call and fills in `content=""` for anything it was
# not given (dash/_pages.py). An empty og:image renders a blank share card,
# which is worse than no tag at all — and `title` is what becomes `og:title`,
# so without the prefix this page's unfurl named no site.
dash.register_page(
    __name__,
    path="/email-builder",
    name="Email Builder",
    title=PAGE_TITLE_PREFIX + "Email Builder",
    description=(
        "AI-powered email template builder: generate dash-email layouts with "
        "Google Gemini, preview them live, export Python code, and send via "
        "Resend."
    ),
    image_url=OG_IMAGE_URL,
)

# Without a Gemini key the builder still works, serving curated example
# templates instead of generating them. Resolved once at import: the key comes
# from the environment and cannot change while the app is running.
AI_ENABLED = is_ai_enabled()

# Email type categories with their options
EMAIL_CATEGORIES = {
    "Marketing & Sales": [
        {"value": "promotional", "label": "Promotional"},
        {"value": "welcome", "label": "Welcome"},
        {"value": "abandoned_cart", "label": "Abandoned Cart"},
        {"value": "re_engagement", "label": "Re-engagement"},
        {"value": "lead_nurturing", "label": "Lead Nurturing"},
        {"value": "newsletter", "label": "Newsletter"},
    ],
    "Transactional": [
        {"value": "transactional", "label": "Transactional"},
        {"value": "onboarding", "label": "Onboarding"},
        {"value": "feedback", "label": "Feedback/Survey"},
        {"value": "announcement", "label": "Announcement"},
        {"value": "milestone", "label": "Milestone"},
    ],
    "Professional": [
        {"value": "personal", "label": "Personal"},
        {"value": "professional", "label": "Professional"},
        {"value": "follow_up", "label": "Follow-Up"},
        {"value": "thank_you", "label": "Thank You"},
    ],
    "Other": [
        {"value": "educational", "label": "Educational"},
        {"value": "invitation", "label": "Invitation"},
    ],
}


def showcase_notice():
    """Explain showcase mode. Renders nothing when AI generation is available."""
    if AI_ENABLED:
        return None
    return dmc.Alert(
        dmc.Stack(
            gap=4,
            children=[
                dmc.Text(
                    "This demo runs without an AI key, so it serves a curated set of example "
                    "templates instead of generating new ones. Everything else is live: each "
                    "example renders through real dash-email components, and the code panel "
                    "shows exactly how it was built.",
                    size="sm",
                ),
                dmc.Text(
                    "Running this yourself? Set GOOGLE_API_KEY to unlock AI generation for "
                    "every email type.",
                    size="sm",
                    c="dimmed",
                ),
            ],
        ),
        title="Showcase mode",
        color="blue",
        variant="light",
        icon=DashIconify(icon="tabler:sparkles", width=20),
        mb="lg",
    )


def create_chip_group(category_name, options):
    """Create a chip group for email category."""
    return dmc.Stack(
        gap="xs",
        children=[
            dmc.Text(category_name, size="sm", fw=500, c="dimmed"),
            dmc.ChipGroup(
                [
                    dmc.Chip(opt["label"], value=opt["value"], size="sm")
                    for opt in options
                ],
                multiple=False,
                id={"type": "email-type-chip", "category": category_name},
            ),
        ],
    )


# Default email preview
default_email = de.Email(
    lang="en",
    children=[
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px",
                                "textAlign": "center",
                            },
                            children=[
                                DashIconify(
                                    icon="tabler:mail-plus",
                                    width=60,
                                    color="#228be6",
                                ),
                                de.EmailHeading(
                                    "Select an email type to get started",
                                    as_="h2",
                                    style={
                                        "color": "#1a1a1a",
                                        "fontSize": "24px",
                                        "margin": "20px 0 10px 0",
                                    },
                                ),
                                de.EmailText(
                                    "Choose an email category, add your requirements, and click Generate to create your email template with AI."
                                    if AI_ENABLED
                                    else "Choose an email type on the left, then load the example to see it rendered here alongside its source code.",
                                    style={
                                        "color": "#666666",
                                        "fontSize": "16px",
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


layout = dmc.Container(
    size="xl",
    py="md",
    children=[
        dmc.Title("Email Builder", order=2, mb="md"),
        dmc.Text(
            "Create professional email templates using AI. Select a type, add your content, and generate."
            if AI_ENABLED
            else "Explore ready-made email templates. Pick a type below to see it rendered live, "
                 "with the dash-email code that produced it.",
            c="dimmed",
            mb="lg",
        ),
        showcase_notice(),

        dmc.Grid(
            gutter="lg",
            children=[
                # Left Panel - Controls
                dmc.GridCol(
                    span={"base": 12, "md": 4},
                    children=[
                        dmc.Paper(
                            p="md",
                            radius="md",
                            withBorder=True,
                            children=[
                                dmc.Stack(
                                    gap="md",
                                    children=[
                                        # Email Type Selection
                                        dmc.Text("Email Type", fw=600, size="lg"),
                                        dmc.Accordion(
                                            variant="separated",
                                            children=[
                                                dmc.AccordionItem(
                                                    value=category,
                                                    children=[
                                                        dmc.AccordionControl(
                                                            category,
                                                            icon=DashIconify(
                                                                icon={
                                                                    "Marketing & Sales": "tabler:chart-line",
                                                                    "Transactional": "tabler:receipt",
                                                                    "Professional": "tabler:briefcase",
                                                                    "Other": "tabler:dots",
                                                                }.get(category, "tabler:mail"),
                                                                width=20,
                                                            ),
                                                        ),
                                                        dmc.AccordionPanel(
                                                            dmc.ChipGroup(
                                                                [
                                                                    dmc.Chip(
                                                                        opt["label"],
                                                                        value=opt["value"],
                                                                        size="sm",
                                                                        # In showcase mode only curated
                                                                        # types can be built.
                                                                        disabled=(
                                                                            not AI_ENABLED
                                                                            and opt["value"] not in SHOWCASE_TYPES
                                                                        ),
                                                                    )
                                                                    for opt in options
                                                                ],
                                                                multiple=False,
                                                                id=f"chip-{category.lower().replace(' ', '-').replace('&', '')}",
                                                            ),
                                                        ),
                                                    ],
                                                )
                                                for category, options in EMAIL_CATEGORIES.items()
                                            ],
                                        ),

                                        # Hidden store for selected email type
                                        dcc.Store(id="selected-email-type", data=""),

                                        dmc.Divider(),

                                        # Content Input
                                        dmc.Text("Your Requirements", fw=600, size="lg"),
                                        dmc.Textarea(
                                            id="email-requirements",
                                            placeholder="Describe your email content, tone, and any specific requirements...\n\nExample: Create a welcome email for a SaaS product called 'TaskFlow'. Include a CTA button to start the free trial. Use a friendly, professional tone.",
                                            minRows=6,
                                            autosize=True,
                                        ),

                                        dmc.Divider(),

                                        # Image Upload
                                        dmc.Text("Images (Optional)", fw=600, size="lg"),
                                        dcc.Upload(
                                            id="image-upload",
                                            children=dmc.Paper(
                                                p="lg",
                                                radius="md",
                                                withBorder=True,
                                                style={
                                                    "borderStyle": "dashed",
                                                    "cursor": "pointer",
                                                    "textAlign": "center",
                                                },
                                                children=[
                                                    DashIconify(
                                                        icon="tabler:upload",
                                                        width=30,
                                                        color="#adb5bd",
                                                    ),
                                                    dmc.Text(
                                                        "Drag & drop or click to upload",
                                                        size="sm",
                                                        c="dimmed",
                                                        mt="xs",
                                                    ),
                                                    dmc.Text(
                                                        "PNG, JPG up to 5MB",
                                                        size="xs",
                                                        c="dimmed",
                                                    ),
                                                ],
                                            ),
                                            multiple=True,
                                            accept="image/*",
                                        ),
                                        html.Div(id="uploaded-images-preview"),

                                        dmc.Divider(),

                                        # Generate Button with loading state
                                        dmc.Button(
                                            "Generate Email" if AI_ENABLED else "Load Example Template",
                                            id="generate-btn",
                                            fullWidth=True,
                                            size="lg",
                                            leftSection=DashIconify(
                                                icon="tabler:sparkles" if AI_ENABLED else "tabler:template",
                                                width=20,
                                            ),
                                            loaderProps={"type": "dots"},
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # Right Panel - Preview and Code
                dmc.GridCol(
                    span={"base": 12, "md": 8},
                    children=[
                        dmc.Tabs(
                            value="preview",
                            children=[
                                dmc.TabsList(
                                    [
                                        dmc.TabsTab(
                                            "Preview",
                                            value="preview",
                                            leftSection=DashIconify(icon="tabler:eye", width=16),
                                        ),
                                        dmc.TabsTab(
                                            "Code",
                                            value="code",
                                            leftSection=DashIconify(icon="tabler:code", width=16),
                                        ),
                                        dmc.TabsTab(
                                            "Send Test",
                                            value="send",
                                            leftSection=DashIconify(icon="tabler:send", width=16),
                                        ),
                                    ],
                                    grow=True,
                                ),

                                # Preview Tab
                                dmc.TabsPanel(
                                    value="preview",
                                    pt="md",
                                    children=[
                                        html.Div(
                                            style={"position": "relative"},
                                            children=[
                                                dmc.LoadingOverlay(
                                                    id="preview-loading-overlay",
                                                    visible=False,
                                                    loaderProps={"type": "dots", "size": "xl"},
                                                    overlayProps={"radius": "md", "blur": 2},
                                                    zIndex=10,
                                                ),
                                                dmc.Paper(
                                                    p=0,
                                                    radius="md",
                                                    withBorder=True,
                                                    style={"overflow": "hidden", "minHeight": "500px"},
                                                    children=[
                                                        html.Div(
                                                            id="email-preview-container",
                                                            style={"backgroundColor": "#f6f9fc"},
                                                            children=[default_email],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),

                                # Code Tab
                                dmc.TabsPanel(
                                    value="code",
                                    pt="md",
                                    children=[
                                        html.Div(
                                            id="code-output-container",
                                            children=[
                                                dmc.Alert(
                                                    "Generate an email to see the code",
                                                    title="No Code Yet",
                                                    color="blue",
                                                    icon=DashIconify(icon="tabler:info-circle"),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),

                                # Send Tab - Mantine-based layout
                                dmc.TabsPanel(
                                    value="send",
                                    pt="md",
                                    children=[
                                        dmc.Grid(
                                            gutter="md",
                                            children=[
                                                # Left Column - Send Options
                                                dmc.GridCol(
                                                    span=6,
                                                    children=[
                                                        dmc.Paper(
                                                            p="md",
                                                            radius="md",
                                                            withBorder=True,
                                                            children=[
                                                                dmc.Tabs(
                                                                    value="single",
                                                                    children=[
                                                                        dmc.TabsList(
                                                                            [
                                                                                dmc.TabsTab("Single", value="single", leftSection=DashIconify(icon="tabler:mail", width=16)),
                                                                                dmc.TabsTab("Batch", value="batch", leftSection=DashIconify(icon="tabler:mail-forward", width=16)),
                                                                            ],
                                                                            grow=True,
                                                                        ),
                                                                        # Single Send Panel
                                                                        dmc.TabsPanel(
                                                                            value="single",
                                                                            pt="md",
                                                                            children=[
                                                                                dmc.Stack(
                                                                                    gap="sm",
                                                                                    children=[
                                                                                        dmc.TextInput(
                                                                                            id="from-email",
                                                                                            label="From",
                                                                                            placeholder="sender@yourdomain.com",
                                                                                            description="Requires verified domain",
                                                                                            value="onboarding@resend.dev",
                                                                                            leftSection=DashIconify(icon="tabler:at", width=16),
                                                                                            size="sm",
                                                                                        ),
                                                                                        dmc.TextInput(
                                                                                            id="recipient-email",
                                                                                            label="To",
                                                                                            placeholder="recipient@example.com",
                                                                                            value="",
                                                                                            leftSection=DashIconify(icon="tabler:mail", width=16),
                                                                                            size="sm",
                                                                                        ),
                                                                                        dmc.TextInput(
                                                                                            id="email-subject",
                                                                                            label="Subject",
                                                                                            placeholder="Email subject",
                                                                                            value="",
                                                                                            leftSection=DashIconify(icon="tabler:text-caption", width=16),
                                                                                            size="sm",
                                                                                        ),
                                                                                        dmc.Group(
                                                                                            gap="xs",
                                                                                            children=[
                                                                                                dcc.Upload(
                                                                                                    id="email-attachments",
                                                                                                    children=dmc.Button(
                                                                                                        "Attach Files",
                                                                                                        variant="light",
                                                                                                        size="xs",
                                                                                                        leftSection=DashIconify(icon="tabler:paperclip", width=14),
                                                                                                    ),
                                                                                                    multiple=True,
                                                                                                ),
                                                                                                html.Div(id="attachment-preview"),
                                                                                            ],
                                                                                        ),
                                                                                        dmc.Button(
                                                                                            "Send Email",
                                                                                            id="send-email-btn",
                                                                                            leftSection=DashIconify(icon="tabler:send", width=16),
                                                                                            disabled=True,
                                                                                            fullWidth=True,
                                                                                        ),
                                                                                        html.Div(id="send-result"),
                                                                                    ],
                                                                                ),
                                                                            ],
                                                                        ),
                                                                        # Batch Send Panel
                                                                        dmc.TabsPanel(
                                                                            value="batch",
                                                                            pt="md",
                                                                            children=[
                                                                                dmc.Stack(
                                                                                    gap="sm",
                                                                                    children=[
                                                                                        dmc.Alert(
                                                                                            "Max 100 recipients. No attachments or scheduling.",
                                                                                            color="blue",
                                                                                            icon=DashIconify(icon="tabler:info-circle"),
                                                                                        ),
                                                                                        dmc.TagsInput(
                                                                                            id="batch-recipients",
                                                                                            label="Recipients",
                                                                                            placeholder="Enter emails, press Enter",
                                                                                            splitChars=[",", " ", ";"],
                                                                                            maxTags=100,
                                                                                            clearable=True,
                                                                                            size="sm",
                                                                                        ),
                                                                                        dmc.Group(
                                                                                            gap="xs",
                                                                                            children=[
                                                                                                dcc.Upload(
                                                                                                    id="csv-recipients-upload",
                                                                                                    children=dmc.Button(
                                                                                                        "Upload CSV",
                                                                                                        variant="light",
                                                                                                        size="xs",
                                                                                                        leftSection=DashIconify(icon="tabler:file-spreadsheet", width=14),
                                                                                                    ),
                                                                                                    accept=".csv",
                                                                                                ),
                                                                                                dmc.Text(id="recipient-count", size="sm", c="dimmed"),
                                                                                            ],
                                                                                        ),
                                                                                        dmc.Button(
                                                                                            "Send Batch",
                                                                                            id="send-batch-btn",
                                                                                            leftSection=DashIconify(icon="tabler:send", width=16),
                                                                                            disabled=True,
                                                                                            fullWidth=True,
                                                                                            color="indigo",
                                                                                        ),
                                                                                        html.Div(id="batch-result"),
                                                                                    ],
                                                                                ),
                                                                            ],
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                # Right Column - Schedule & Templates
                                                dmc.GridCol(
                                                    span=6,
                                                    children=[
                                                        dmc.Paper(
                                                            p="md",
                                                            radius="md",
                                                            withBorder=True,
                                                            children=[
                                                                dmc.Tabs(
                                                                    value="schedule",
                                                                    children=[
                                                                        dmc.TabsList(
                                                                            [
                                                                                dmc.TabsTab("Schedule", value="schedule", leftSection=DashIconify(icon="tabler:calendar-time", width=16)),
                                                                                dmc.TabsTab("Templates", value="templates", leftSection=DashIconify(icon="tabler:template", width=16)),
                                                                            ],
                                                                            grow=True,
                                                                        ),
                                                                        # Schedule Panel
                                                                        dmc.TabsPanel(
                                                                            value="schedule",
                                                                            pt="md",
                                                                            children=[
                                                                                dmc.Stack(
                                                                                    gap="sm",
                                                                                    children=[
                                                                                        dmc.Alert(
                                                                                            "Schedule up to 30 days ahead. Single send only.",
                                                                                            color="blue",
                                                                                            icon=DashIconify(icon="tabler:calendar-time"),
                                                                                        ),
                                                                                        dmc.Checkbox(
                                                                                            id="schedule-enabled",
                                                                                            label="Enable scheduling",
                                                                                            size="sm",
                                                                                        ),
                                                                                        dmc.DateTimePicker(
                                                                                            id="schedule-datetime",
                                                                                            label="Date & Time",
                                                                                            placeholder="Select date and time",
                                                                                            clearable=True,
                                                                                            disabled=True,
                                                                                            size="sm",
                                                                                        ),
                                                                                        dmc.Divider(label="Or natural language", labelPosition="center"),
                                                                                        dmc.TextInput(
                                                                                            id="schedule-natural",
                                                                                            placeholder="e.g., 'tomorrow at 9am'",
                                                                                            value="",
                                                                                            leftSection=DashIconify(icon="tabler:clock", width=16),
                                                                                            disabled=True,
                                                                                            size="sm",
                                                                                        ),
                                                                                    ],
                                                                                ),
                                                                            ],
                                                                        ),
                                                                        # Templates Panel
                                                                        dmc.TabsPanel(
                                                                            value="templates",
                                                                            pt="md",
                                                                            children=[
                                                                                dmc.Stack(
                                                                                    gap="sm",
                                                                                    children=[
                                                                                        dmc.TextInput(
                                                                                            id="template-name",
                                                                                            label="Template Name",
                                                                                            placeholder="e.g., Welcome Email v1",
                                                                                            value="",
                                                                                            leftSection=DashIconify(icon="tabler:file-text", width=16),
                                                                                            size="sm",
                                                                                        ),
                                                                                        dmc.Button(
                                                                                            "Save as Template",
                                                                                            id="save-template-btn",
                                                                                            leftSection=DashIconify(icon="tabler:device-floppy", width=16),
                                                                                            variant="outline",
                                                                                            fullWidth=True,
                                                                                        ),
                                                                                        html.Div(id="template-save-result"),
                                                                                        dmc.Divider(label="Saved Templates", labelPosition="center"),
                                                                                        dmc.Group(
                                                                                            gap="xs",
                                                                                            grow=True,
                                                                                            children=[
                                                                                                dmc.Select(
                                                                                                    id="template-select",
                                                                                                    placeholder="Choose template",
                                                                                                    data=[],
                                                                                                    clearable=True,
                                                                                                    size="sm",
                                                                                                    style={"flex": 1},
                                                                                                ),
                                                                                                dmc.ActionIcon(
                                                                                                    DashIconify(icon="tabler:refresh", width=16),
                                                                                                    id="refresh-templates-btn",
                                                                                                    variant="light",
                                                                                                    size="lg",
                                                                                                ),
                                                                                            ],
                                                                                        ),
                                                                                    ],
                                                                                ),
                                                                            ],
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # Store for generated code
        dcc.Store(id="generated-code-store", data={}),
        dcc.Store(id="uploaded-images-store", data=[]),
        dcc.Store(id="file-attachments-store", data=[]),
    ],
)


# Callbacks
@callback(
    Output("selected-email-type", "data"),
    [
        Input("chip-marketing--sales", "value"),
        Input("chip-transactional", "value"),
        Input("chip-professional", "value"),
        Input("chip-other", "value"),
    ],
    prevent_initial_call=True,
)
def update_selected_type(marketing, transactional, professional, other):
    """Update the selected email type from any chip group."""
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    # Get the value from whichever input triggered
    for marketing_val, trans_val, prof_val, other_val in [(marketing, transactional, professional, other)]:
        if marketing_val:
            return marketing_val
        if trans_val:
            return trans_val
        if prof_val:
            return prof_val
        if other_val:
            return other_val

    # Return the actual triggered value
    triggered_value = ctx.triggered[0]["value"]
    return triggered_value if triggered_value else no_update


@callback(
    Output("uploaded-images-preview", "children"),
    Output("uploaded-images-store", "data"),
    Input("image-upload", "contents"),
    State("image-upload", "filename"),
    prevent_initial_call=True,
)
def preview_uploaded_images(contents, filenames):
    """Save uploaded images locally and preview them."""
    if not contents:
        return None, []

    # Clean up old uploads (older than 24 hours)
    cleanup_old_uploads(max_age_hours=24)

    # Save images to disk and get URLs
    saved_urls = save_multiple_images(contents, filenames)

    previews = []
    for url, filename in zip(saved_urls, filenames):
        previews.append(
            dmc.Group(
                gap="xs",
                mt="xs",
                children=[
                    dmc.Image(
                        src=url,  # Use saved URL instead of base64
                        h=50,
                        w=50,
                        radius="sm",
                        fit="cover",
                    ),
                    dmc.Text(filename, size="xs", truncate=True),
                ],
            )
        )

    # Store URLs instead of base64 data
    return dmc.Stack(gap="xs", children=previews), saved_urls


# Clientside callback to immediately show loading state when button is clicked
clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            return [true, true];
        }
        return [false, false];
    }
    """,
    Output("generate-btn", "loading"),
    Output("preview-loading-overlay", "visible"),
    Input("generate-btn", "n_clicks"),
    prevent_initial_call=True,
)


@callback(
    Output("email-preview-container", "children"),
    Output("code-output-container", "children"),
    Output("generated-code-store", "data"),
    Output("email-subject", "value"),
    Output("send-email-btn", "disabled"),
    Output("generate-btn", "loading", allow_duplicate=True),
    Output("preview-loading-overlay", "visible", allow_duplicate=True),
    Input("generate-btn", "n_clicks"),
    State("selected-email-type", "data"),
    State("email-requirements", "value"),
    State("uploaded-images-store", "data"),
    prevent_initial_call=True,
)
def generate_email(n_clicks, email_type, requirements, image_urls):
    """Generate an email with Gemini, or serve a curated example without a key."""
    if not n_clicks:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if not email_type:
        return (
            dmc.Alert(
                "Please select an email type first",
                title="Selection Required",
                color="yellow",
                icon=DashIconify(icon="tabler:alert-circle"),
            ),
            no_update,
            no_update,
            no_update,
            True,
            False,  # Stop button loading
            False,  # Hide overlay
        )

    try:
        if AI_ENABLED:
            from utils.gemini_handler import generate_email_content

            # Generate email content with image URLs
            result = generate_email_content(
                email_type=email_type,
                user_content=requirements or "",
                image_urls=image_urls if image_urls else None,
            )
        else:
            from utils.showcase_templates import get_showcase_template

            result = get_showcase_template(email_type)

        if "error" in result:
            # A missing showcase template is an expected limit of demo mode,
            # not a failure — say so rather than crying error.
            return (
                dmc.Alert(
                    result["error"] if not AI_ENABLED
                    else f"Error generating email: {result['error']}",
                    title="No example for this type" if not AI_ENABLED else "Generation Error",
                    color="yellow" if not AI_ENABLED else "red",
                    icon=DashIconify(
                        icon="tabler:info-circle" if not AI_ENABLED else "tabler:alert-triangle"
                    ),
                ),
                no_update,
                {},
                "",
                True,
                False,  # Stop button loading
                False,  # Hide overlay
            )

        # Create preview by executing the preview code
        preview_component = create_preview_from_code(result.get("preview_code", ""))

        # Create code display with unique key to force remount on update
        code_display = html.Div(
            key=str(uuid.uuid4()),
            children=[
                dmc.CodeHighlightTabs(
                    code=[
                        {
                            "fileName": "email_template.py",
                            "code": result.get("full_code", "# No code generated"),
                            "language": "python",
                        },
                    ],
                    withExpandButton=True,
                    defaultExpanded=True,
                ),
            ],
        )

        return (
            preview_component if preview_component else default_email,
            code_display,
            result,
            result.get("subject", ""),
            False,
            False,  # Stop button loading
            False,  # Hide overlay
        )

    except Exception as e:
        return (
            dmc.Alert(
                f"Error: {str(e)}",
                title="Error",
                color="red",
                icon=DashIconify(icon="tabler:alert-triangle"),
            ),
            no_update,
            {},
            "",
            True,
            False,  # Stop button loading
            False,  # Hide overlay
        )


def create_preview_from_code(preview_code: str):
    """
    Create a preview component from the generated code.
    This executes the code safely to generate the component.
    """
    if not preview_code or preview_code.startswith("# Error"):
        return None

    try:
        # Create a safe execution environment
        local_vars = {"de": de, "DashIconify": DashIconify}

        # Clean up the code
        code = preview_code.strip()

        # Ensure the code starts with de.Email
        if not code.startswith("de.Email"):
            # Try to find de.Email in the code
            email_start = code.find("de.Email(")
            if email_start >= 0:
                code = code[email_start:]
            else:
                print(f"Preview code doesn't contain de.Email: {code[:100]}...")
                return None

        # Execute and get the result
        exec(f"result = {code}", {"de": de, "DashIconify": DashIconify}, local_vars)

        return local_vars.get("result")
    except SyntaxError as e:
        print(f"Syntax error in preview code: {e}")
        print(f"Code snippet: {code[:200] if code else 'empty'}...")
        return dmc.Alert(
            "Could not render preview due to syntax error. The email was still generated - check the Code tab.",
            title="Preview Error",
            color="orange",
        )
    except Exception as e:
        print(f"Error creating preview: {e}")
        return dmc.Alert(
            f"Could not render preview: {str(e)}",
            title="Preview Error",
            color="orange",
        )


@callback(
    Output("send-result", "children"),
    Input("send-email-btn", "n_clicks"),
    State("recipient-email", "value"),
    State("email-subject", "value"),
    State("from-email", "value"),
    State("generated-code-store", "data"),
    State("file-attachments-store", "data"),
    State("schedule-enabled", "checked"),
    State("schedule-datetime", "value"),
    State("schedule-natural", "value"),
    prevent_initial_call=True,
)
def send_test_email(n_clicks, recipient, subject, from_email, code_data, file_attachments,
                    schedule_enabled, schedule_datetime, schedule_natural):
    """Send a test email via Resend with scheduling and attachments."""
    if not n_clicks or not recipient:
        return no_update

    if not code_data or not code_data.get("full_code"):
        return dmc.Alert(
            "Please generate an email first",
            color="yellow",
        )

    try:
        from utils.email_sender import send_email, generate_html_from_code

        # Generate HTML from the full email code
        html_content = generate_html_from_code(
            code_data.get("full_code", ""),
            base_url=""  # Keep relative URLs for CID embedding
        )

        # Determine scheduled_at value
        scheduled_at = None
        if schedule_enabled:
            if schedule_natural:
                scheduled_at = schedule_natural  # Natural language like "tomorrow at 9am"
            elif schedule_datetime:
                scheduled_at = schedule_datetime  # ISO format from DateTimePicker

        result = send_email(
            to_email=recipient,
            subject=subject or "Test Email from Dash Email",
            html_content=html_content,
            from_email=from_email or "onboarding@resend.dev",
            scheduled_at=scheduled_at,
            file_attachments=file_attachments if file_attachments else None,
        )

        if result["success"]:
            # Build detailed success message
            inline_count = result.get("inline_images", 0)
            file_count = result.get("file_attachments", 0)
            message = result["message"]

            details = []
            if inline_count > 0:
                details.append(f"{inline_count} images embedded")
            if file_count > 0:
                details.append(f"{file_count} files attached")
            if details:
                message += f" ({', '.join(details)})"

            return dmc.Alert(
                message,
                title="Success!" if not scheduled_at else "Scheduled!",
                color="green",
                icon=DashIconify(icon="tabler:check" if not scheduled_at else "tabler:calendar-check"),
            )
        else:
            return dmc.Alert(
                result["error"],
                title="Failed to Send",
                color="red",
                icon=DashIconify(icon="tabler:x"),
            )

    except Exception as e:
        return dmc.Alert(
            str(e),
            title="Error",
            color="red",
        )


# ============ NEW CALLBACKS ============

# File attachment preview
@callback(
    Output("attachment-preview", "children"),
    Output("file-attachments-store", "data"),
    Input("email-attachments", "contents"),
    State("email-attachments", "filename"),
    prevent_initial_call=True,
)
def preview_file_attachments(contents, filenames):
    """Preview uploaded file attachments."""
    if not contents:
        return None, []

    attachments = []
    previews = []

    for content, filename in zip(contents, filenames):
        # Extract base64 content
        content_string = content.split(",")[1] if "," in content else content

        attachments.append({
            "content": content_string,
            "filename": filename,
        })

        previews.append(
            dmc.Group(
                gap="xs",
                children=[
                    DashIconify(icon="tabler:file", width=20, color="#868e96"),
                    dmc.Text(filename, size="sm", truncate=True),
                ],
            )
        )

    return dmc.Stack(gap="xs", children=previews), attachments


# CSV recipients parsing
@callback(
    Output("batch-recipients", "value"),
    Input("csv-recipients-upload", "contents"),
    State("csv-recipients-upload", "filename"),
    prevent_initial_call=True,
)
def parse_csv_recipients(contents, filename):
    """Parse CSV file to extract email addresses."""
    if not contents:
        return no_update

    try:
        import pandas as pd

        content_string = contents.split(",")[1]
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        # Find email column (look for 'email', 'Email', 'EMAIL', etc.)
        email_col = None
        for col in df.columns:
            if "email" in col.lower():
                email_col = col
                break

        if email_col:
            emails = df[email_col].dropna().tolist()[:100]  # Max 100
            return emails
        else:
            # If no email column, try first column
            emails = df.iloc[:, 0].dropna().tolist()[:100]
            return emails

    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return []


# Recipient count display
@callback(
    Output("recipient-count", "children"),
    Output("send-batch-btn", "disabled"),
    Input("batch-recipients", "value"),
    State("generated-code-store", "data"),
)
def update_recipient_count(recipients, code_data):
    """Update recipient count and enable/disable batch button."""
    count = len(recipients) if recipients else 0
    has_code = code_data and code_data.get("full_code")

    return f"{count} recipients", not (count > 0 and has_code)


# Schedule enable/disable
@callback(
    Output("schedule-datetime", "disabled"),
    Output("schedule-natural", "disabled"),
    Input("schedule-enabled", "checked"),
)
def toggle_schedule_inputs(enabled):
    """Enable/disable schedule inputs based on checkbox."""
    return not enabled, not enabled


# Batch send
@callback(
    Output("batch-result", "children"),
    Input("send-batch-btn", "n_clicks"),
    State("batch-recipients", "value"),
    State("email-subject", "value"),
    State("from-email", "value"),
    State("generated-code-store", "data"),
    prevent_initial_call=True,
)
def send_batch_email(n_clicks, recipients, subject, from_email, code_data):
    """Send batch emails via Resend."""
    if not n_clicks or not recipients:
        return no_update

    if not code_data or not code_data.get("full_code"):
        return dmc.Alert(
            "Please generate an email first",
            color="yellow",
        )

    try:
        from utils.email_sender import send_batch_emails, generate_html_from_code

        # Generate HTML
        html_content = generate_html_from_code(
            code_data.get("full_code", ""),
            base_url=""
        )

        result = send_batch_emails(
            recipients=recipients,
            subject=subject or "Email from Dash Email",
            html_content=html_content,
            from_email=from_email or "onboarding@resend.dev",
        )

        if result["success"]:
            return dmc.Alert(
                result["message"],
                title="Batch Sent!",
                color="green",
                icon=DashIconify(icon="tabler:checks"),
            )
        else:
            return dmc.Alert(
                result["error"],
                title="Batch Failed",
                color="red",
                icon=DashIconify(icon="tabler:x"),
            )

    except Exception as e:
        return dmc.Alert(
            str(e),
            title="Error",
            color="red",
        )


# Save template
@callback(
    Output("template-save-result", "children"),
    Input("save-template-btn", "n_clicks"),
    State("template-name", "value"),
    State("email-subject", "value"),
    State("generated-code-store", "data"),
    State("from-email", "value"),
    prevent_initial_call=True,
)
def save_template(n_clicks, template_name, subject, code_data, from_email):
    """Save current email as a Resend template."""
    if not n_clicks:
        return no_update

    if not template_name:
        return dmc.Alert(
            "Please enter a template name",
            color="yellow",
        )

    if not code_data or not code_data.get("full_code"):
        return dmc.Alert(
            "Please generate an email first",
            color="yellow",
        )

    try:
        from utils.template_handler import create_template
        from utils.email_sender import generate_html_from_code

        # Generate HTML
        html_content = generate_html_from_code(
            code_data.get("full_code", ""),
            base_url=""
        )

        result = create_template(
            name=template_name,
            subject=subject or "Email Template",
            html=html_content,
            from_email=from_email or "onboarding@resend.dev",
        )

        if result["success"]:
            return dmc.Alert(
                result["message"],
                title="Template Saved!",
                color="green",
                icon=DashIconify(icon="tabler:check"),
            )
        else:
            return dmc.Alert(
                result["error"],
                title="Save Failed",
                color="red",
                icon=DashIconify(icon="tabler:x"),
            )

    except Exception as e:
        return dmc.Alert(
            str(e),
            title="Error",
            color="red",
        )


# Refresh templates list
@callback(
    Output("template-select", "data"),
    Input("refresh-templates-btn", "n_clicks"),
    prevent_initial_call=True,
)
def refresh_templates(n_clicks):
    """Refresh the list of available templates from Resend."""
    if not n_clicks:
        return no_update

    try:
        from utils.template_handler import list_templates

        result = list_templates()

        if result["success"]:
            templates = result.get("templates", [])
            return [
                {"value": t.get("id", ""), "label": t.get("name", "Unknown")}
                for t in templates
            ]
        else:
            return []

    except Exception as e:
        print(f"Error loading templates: {e}")
        return []
