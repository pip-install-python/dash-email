import dash_email as de

component = de.Email([
    de.EmailBody(
        style={"backgroundColor": "#eef2f6", "padding": "32px 0"},
        children=[
            de.EmailContainer(
                style={"maxWidth": "600px"},
                children=[
                    de.EmailSection(
                        style={
                            "backgroundColor": "#1a1a2e",
                            "padding": "24px",
                            "textAlign": "center",
                            "borderRadius": "8px 8px 0 0",
                        },
                        children=[
                            de.EmailHeading(
                                "Header Section",
                                as_="h3",
                                style={"color": "#ffffff", "margin": 0},
                            ),
                        ],
                    ),
                    de.EmailSection(
                        style={"backgroundColor": "#ffffff", "padding": "24px"},
                        children=[
                            de.EmailText(
                                "EmailContainer centers content at 600px — the "
                                "de-facto standard email width. EmailSection "
                                "groups related blocks so each area can carry "
                                "its own background and padding."
                            ),
                        ],
                    ),
                    de.EmailSection(
                        style={
                            "backgroundColor": "#f8f9fa",
                            "padding": "16px 24px",
                            "textAlign": "center",
                            "borderRadius": "0 0 8px 8px",
                        },
                        children=[
                            de.EmailText(
                                "Footer section",
                                style={"color": "#999999", "fontSize": "12px", "margin": 0},
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
])
