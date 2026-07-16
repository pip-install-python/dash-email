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
                        de.EmailImage(
                            src="https://picsum.photos/seed/dash-email/536/200",
                            alt="Hero banner",
                            width=536,
                            height=200,
                            style={"borderRadius": "8px", "maxWidth": "100%"},
                        ),
                        de.EmailHeading("Hero images", as_="h3"),
                        de.EmailText(
                            "Always set explicit width/height and an alt text — "
                            "many clients block images until the reader opts in."
                        ),
                        de.EmailDivider(
                            style={"borderColor": "#dee2e6", "margin": "24px 0"}
                        ),
                        de.EmailText(
                            "EmailDivider renders an <hr> to separate content "
                            "blocks.",
                            style={"color": "#868e96"},
                        ),
                    ],
                )
            ])
        ],
    )
])
