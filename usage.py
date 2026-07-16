"""
Example usage of dash_email components.

This demonstrates how to build email templates using Dash components
that wrap React Email.

Run with: python usage.py
"""
import dash
from dash import html
import dash_mantine_components as dmc
import dash_email as de

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ]
)

# Example email template code for display
example_email_code = '''import dash_email as de

email = de.Email(
    lang="en",
    children=[
        de.EmailPreview("Welcome to our platform!"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc"},
            children=[
                de.EmailContainer(
                    style={"padding": "20px 0"},
                    children=[
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px"
                            },
                            children=[
                                de.EmailHeading(
                                    "Welcome aboard!",
                                    as_="h1",
                                    style={"color": "#1a1a1a", "fontSize": "24px"}
                                ),
                                de.EmailText(
                                    "Thanks for signing up!",
                                    style={"color": "#666666", "fontSize": "16px"}
                                ),
                                de.EmailButton(
                                    "Get Started",
                                    href="https://example.com/dashboard",
                                    style={
                                        "backgroundColor": "#007bff",
                                        "color": "#ffffff",
                                        "padding": "12px 24px",
                                        "borderRadius": "6px"
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)'''

# Build the actual email template using dash_email components
email_preview = de.Email(
    lang="en",
    children=[
        de.EmailPreview("Welcome to our platform!"),
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "fontFamily": "Inter, sans-serif"},
            children=[
                de.EmailContainer(
                    style={"padding": "40px 20px", "maxWidth": "600px"},
                    children=[
                        # Logo/Header Section
                        de.EmailSection(
                            style={"textAlign": "center", "marginBottom": "30px"},
                            children=[
                                de.EmailImage(
                                    src="https://react.email/static/icons/logo.png",
                                    width=50,
                                    alt="Logo"
                                )
                            ]
                        ),

                        # Main Content Card
                        de.EmailSection(
                            style={
                                "backgroundColor": "#ffffff",
                                "borderRadius": "8px",
                                "padding": "40px",
                                "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"
                            },
                            children=[
                                de.EmailHeading(
                                    "Welcome aboard!",
                                    as_="h1",
                                    style={
                                        "color": "#1a1a1a",
                                        "fontSize": "28px",
                                        "fontWeight": "600",
                                        "margin": "0 0 16px 0"
                                    }
                                ),
                                de.EmailText(
                                    "Thanks for signing up. We're thrilled to have you join us. "
                                    "Click the button below to get started with your account.",
                                    style={
                                        "color": "#666666",
                                        "fontSize": "16px",
                                        "lineHeight": "26px",
                                        "margin": "0 0 24px 0"
                                    }
                                ),
                                de.EmailButton(
                                    "Get Started",
                                    href="https://example.com/dashboard",
                                    style={
                                        "backgroundColor": "#228be6",
                                        "color": "#ffffff",
                                        "padding": "14px 28px",
                                        "borderRadius": "6px",
                                        "textDecoration": "none",
                                        "fontWeight": "500",
                                        "fontSize": "16px",
                                        "display": "inline-block"
                                    }
                                )
                            ]
                        ),

                        # Features Section - Two Columns
                        de.EmailSection(
                            style={"marginTop": "30px"},
                            children=[
                                de.EmailRow([
                                    de.EmailColumn(
                                        style={
                                            "width": "50%",
                                            "padding": "15px",
                                            "backgroundColor": "#ffffff",
                                            "borderRadius": "6px"
                                        },
                                        children=[
                                            de.EmailHeading(
                                                "Fast Setup",
                                                as_="h3",
                                                style={"fontSize": "16px", "margin": "0 0 8px 0"}
                                            ),
                                            de.EmailText(
                                                "Get up and running in minutes",
                                                style={"fontSize": "14px", "color": "#666", "margin": "0"}
                                            )
                                        ]
                                    ),
                                    de.EmailColumn(
                                        style={
                                            "width": "50%",
                                            "padding": "15px",
                                            "backgroundColor": "#ffffff",
                                            "borderRadius": "6px"
                                        },
                                        children=[
                                            de.EmailHeading(
                                                "Great Support",
                                                as_="h3",
                                                style={"fontSize": "16px", "margin": "0 0 8px 0"}
                                            ),
                                            de.EmailText(
                                                "We're here to help 24/7",
                                                style={"fontSize": "14px", "color": "#666", "margin": "0"}
                                            )
                                        ]
                                    )
                                ])
                            ]
                        ),

                        # Footer
                        de.EmailSection(
                            style={"marginTop": "40px", "textAlign": "center"},
                            children=[
                                de.EmailDivider(
                                    style={"borderColor": "#e6e6e6", "margin": "0 0 20px 0"}
                                ),
                                de.EmailText(
                                    children=[
                                        de.EmailLink(
                                            "Unsubscribe",
                                            href="https://example.com/unsubscribe",
                                            style={"color": "#666666", "fontSize": "12px"}
                                        ),
                                        " | ",
                                        de.EmailLink(
                                            "Privacy Policy",
                                            href="https://example.com/privacy",
                                            style={"color": "#666666", "fontSize": "12px"}
                                        ),
                                        " | ",
                                        de.EmailLink(
                                            "View in Browser",
                                            href="https://example.com/email/view",
                                            style={"color": "#666666", "fontSize": "12px"}
                                        )
                                    ],
                                    style={"margin": "0"}
                                ),
                                de.EmailText(
                                    "123 Main Street, City, ST 12345",
                                    style={
                                        "color": "#999999",
                                        "fontSize": "12px",
                                        "marginTop": "10px"
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


def _component_card(name, description):
    """Create a card displaying component info."""
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="sm",
        children=[
            dmc.Text(name, fw=500, size="sm"),
            dmc.Text(description, size="xs", c="dimmed")
        ]
    )


app.layout = dmc.MantineProvider(
    children=[
        dmc.Container(
            size="lg",
            py="xl",
            children=[
                dmc.Title("dash-email", order=1, mb="xs"),
                dmc.Text(
                    "Build email templates with React Email components in Dash",
                    c="dimmed",
                    size="lg",
                    mb="xl"
                ),

                dmc.Tabs(
                    value="preview",
                    children=[
                        dmc.TabsList([
                            dmc.TabsTab("Live Preview", value="preview"),
                            dmc.TabsTab("Code Example", value="code"),
                            dmc.TabsTab("All Components", value="components"),
                        ]),

                        dmc.TabsPanel(
                            value="preview",
                            pt="md",
                            children=[
                                dmc.Paper(
                                    withBorder=True,
                                    p=0,
                                    radius="md",
                                    style={"overflow": "hidden"},
                                    children=[
                                        # Email preview rendered with dash_email components
                                        html.Div(
                                            email_preview,
                                            style={
                                                "backgroundColor": "#f6f9fc",
                                                "minHeight": "600px"
                                            }
                                        )
                                    ]
                                )
                            ]
                        ),

                        dmc.TabsPanel(
                            value="code",
                            pt="md",
                            children=[
                                dmc.CodeHighlight(
                                    code=example_email_code,
                                    language="python",
                                )
                            ]
                        ),

                        dmc.TabsPanel(
                            value="components",
                            pt="md",
                            children=[
                                dmc.Text(
                                    "Available Components",
                                    fw=500,
                                    mb="md"
                                ),
                                dmc.SimpleGrid(
                                    cols={"base": 2, "sm": 3, "lg": 5},
                                    spacing="sm",
                                    children=[
                                        _component_card(name, desc)
                                        for name, desc in [
                                            ("Email", "Root wrapper"),
                                            ("EmailHead", "Metadata"),
                                            ("EmailBody", "Body wrapper"),
                                            ("EmailPreview", "Preview text"),
                                            ("EmailContainer", "Centered container"),
                                            ("EmailSection", "Content group"),
                                            ("EmailRow", "Horizontal row"),
                                            ("EmailColumn", "Column"),
                                            ("EmailButton", "CTA button"),
                                            ("EmailLink", "Hyperlink"),
                                            ("EmailText", "Paragraph"),
                                            ("EmailHeading", "H1-H6"),
                                            ("EmailImage", "Image"),
                                            ("EmailDivider", "HR line"),
                                            ("EmailFont", "Custom font"),
                                        ]
                                    ]
                                )
                            ]
                        ),
                    ]
                ),

                dmc.Space(h="xl"),

                dmc.Alert(
                    title="Getting Started",
                    color="blue",
                    children=[
                        dmc.Text([
                            "Install: ",
                            dmc.Code("pip install dash-email"),
                        ], size="sm"),
                        dmc.Text([
                            "Import: ",
                            dmc.Code("import dash_email as de"),
                        ], size="sm", mt="xs"),
                    ]
                )
            ]
        )
    ]
)


if __name__ == '__main__':
    app.run(debug=True, port=8050)