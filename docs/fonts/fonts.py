import dash_email as de

component = de.Email([
    de.EmailHead(
        children=[
            de.EmailFont(
                fontFamily="Roboto",
                fallbackFontFamily="Verdana",
                webFont={
                    "url": "https://fonts.gstatic.com/s/roboto/v27/KFOmCnqEu92Fr1Mu4mxKKTU1Kg.woff2",
                    "format": "woff2",
                },
                fontWeight=400,
                fontStyle="normal",
            ),
        ],
    ),
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
                        de.EmailHeading(
                            "Custom web fonts",
                            as_="h3",
                            style={"fontFamily": "Roboto, Verdana, sans-serif"},
                        ),
                        de.EmailText(
                            "EmailFont registers a web font with a fallback "
                            "family. Clients that support web fonts (Apple "
                            "Mail, iOS) load it; everyone else falls back "
                            "gracefully.",
                            style={"fontFamily": "Roboto, Verdana, sans-serif"},
                        ),
                    ],
                )
            ])
        ],
    ),
])
