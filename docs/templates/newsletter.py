import dash_email as de

component = de.Email([
    de.EmailPreview("This week's top stories and updates"),
    de.EmailBody(
        style={"backgroundColor": "#f0f0f0", "padding": "24px 0"},
        children=[
            de.EmailContainer([
                # Header
                de.EmailSection(
                    style={
                        "backgroundColor": "#1a1a2e",
                        "padding": "30px",
                        "textAlign": "center",
                        "borderRadius": "8px 8px 0 0",
                    },
                    children=[
                        de.EmailHeading(
                            "Weekly Newsletter",
                            as_="h1",
                            style={"color": "#ffffff", "margin": 0},
                        )
                    ],
                ),
                # Content
                de.EmailSection(
                    style={"backgroundColor": "#ffffff", "padding": "40px"},
                    children=[
                        de.EmailHeading("Featured Article", as_="h2"),
                        de.EmailText(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing "
                            "elit. Sed do eiusmod tempor incididunt ut labore et "
                            "dolore magna aliqua.",
                            style={"lineHeight": "1.7", "color": "#495057"},
                        ),
                        de.EmailButton(
                            "Read More",
                            href="https://example.com",
                            style={
                                "backgroundColor": "#228be6",
                                "color": "#ffffff",
                                "padding": "10px 24px",
                                "borderRadius": "4px",
                            },
                        ),
                        de.EmailDivider(style={"margin": "30px 0"}),
                        de.EmailHeading("Quick Links", as_="h3"),
                        de.EmailText([
                            de.EmailLink(
                                "Product updates",
                                href="https://example.com",
                                style={"color": "#1971c2"},
                            ),
                            " · ",
                            de.EmailLink(
                                "Community forum",
                                href="https://example.com",
                                style={"color": "#1971c2"},
                            ),
                            " · ",
                            de.EmailLink(
                                "Blog",
                                href="https://example.com",
                                style={"color": "#1971c2"},
                            ),
                        ]),
                    ],
                ),
                # Footer
                de.EmailSection(
                    style={
                        "padding": "20px",
                        "textAlign": "center",
                        "borderRadius": "0 0 8px 8px",
                        "backgroundColor": "#f8f9fa",
                    },
                    children=[
                        de.EmailText(
                            "You received this because you subscribed. "
                            "Unsubscribe at any time.",
                            style={"color": "#999999", "fontSize": "12px"},
                        )
                    ],
                ),
            ])
        ],
    ),
])
