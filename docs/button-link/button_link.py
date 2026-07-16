import dash_email as de

component = de.Email([
    de.EmailBody(
        style={"backgroundColor": "#f6f9fc", "padding": "32px 0"},
        children=[
            de.EmailContainer([
                de.EmailSection(
                    style={
                        "backgroundColor": "#ffffff",
                        "borderRadius": "8px",
                        "padding": "32px",
                        "textAlign": "center",
                    },
                    children=[
                        de.EmailHeading("Call to action", as_="h3"),
                        de.EmailText(
                            "EmailButton is a styled link that renders as a "
                            "bulletproof button in every client."
                        ),
                        de.EmailButton(
                            "Primary Action",
                            href="https://example.com",
                            style={
                                "backgroundColor": "#228be6",
                                "color": "#ffffff",
                                "padding": "12px 28px",
                                "borderRadius": "6px",
                                "fontWeight": "bold",
                            },
                        ),
                        de.EmailText(" "),
                        de.EmailButton(
                            "Secondary Action",
                            href="https://example.com",
                            style={
                                "backgroundColor": "#ffffff",
                                "color": "#228be6",
                                "padding": "12px 28px",
                                "borderRadius": "6px",
                                "fontWeight": "bold",
                                "border": "2px solid #228be6",
                            },
                        ),
                        de.EmailDivider(style={"margin": "24px 0"}),
                        de.EmailText([
                            "Inline links use EmailLink — ",
                            de.EmailLink(
                                "read the full story",
                                href="https://example.com",
                                style={"color": "#228be6"},
                            ),
                            ".",
                        ]),
                    ],
                )
            ])
        ],
    )
])
