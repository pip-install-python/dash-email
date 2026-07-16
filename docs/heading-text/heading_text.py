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
                    },
                    children=[
                        de.EmailHeading("Heading level h1", as_="h1"),
                        de.EmailHeading("Heading level h2", as_="h2"),
                        de.EmailHeading(
                            "Styled h3 heading",
                            as_="h3",
                            style={"color": "#228be6", "letterSpacing": "1px"},
                        ),
                        de.EmailText(
                            "EmailText renders paragraph copy. Use the style "
                            "prop for color, size, and line height — all "
                            "rendered inline for email-client safety.",
                            style={"color": "#495057", "lineHeight": "1.7"},
                        ),
                        de.EmailText(
                            "Small, muted footnote text.",
                            style={"color": "#999999", "fontSize": "12px"},
                        ),
                    ],
                )
            ])
        ],
    )
])
