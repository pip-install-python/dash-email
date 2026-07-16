import dash_email as de

component = de.Email(
    lang="en",
    children=[
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "padding": "40px 0"},
            children=[
                de.EmailContainer([
                    de.EmailSection(
                        style={
                            "backgroundColor": "#ffffff",
                            "borderRadius": "8px",
                            "padding": "40px",
                        },
                        children=[
                            de.EmailHeading(
                                "Welcome!",
                                as_="h1",
                                style={"color": "#1a1a1a", "marginBottom": "16px"},
                            ),
                            de.EmailText(
                                "Thanks for signing up. We're excited to have you!",
                                style={"color": "#666666", "lineHeight": "1.6"},
                            ),
                            de.EmailButton(
                                "Get Started",
                                href="https://example.com",
                                style={
                                    "backgroundColor": "#228be6",
                                    "color": "#ffffff",
                                    "padding": "12px 24px",
                                    "borderRadius": "4px",
                                    "fontWeight": "bold",
                                },
                            ),
                        ],
                    )
                ])
            ],
        )
    ],
)
