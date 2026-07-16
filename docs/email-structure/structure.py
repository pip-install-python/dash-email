import dash_email as de

component = de.Email(
    lang="en",
    dir="ltr",
    children=[
        de.EmailHead(),
        de.EmailPreview("Your March summary is ready — open to see the highlights."),
        de.EmailBody(
            style={"backgroundColor": "#f0f4f8", "padding": "32px 0"},
            children=[
                de.EmailContainer([
                    de.EmailSection(
                        style={
                            "backgroundColor": "#ffffff",
                            "borderRadius": "8px",
                            "padding": "32px",
                        },
                        children=[
                            de.EmailHeading("Monthly Update", as_="h2"),
                            de.EmailText(
                                "The preview text above is hidden in the rendered "
                                "email body but shows next to the subject line in "
                                "the recipient's inbox."
                            ),
                        ],
                    )
                ])
            ],
        ),
    ],
)
