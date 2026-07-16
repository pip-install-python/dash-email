import dash_email as de

CELL = {"padding": "12px", "verticalAlign": "top"}

component = de.Email([
    de.EmailBody(
        style={"backgroundColor": "#f6f9fc", "padding": "32px 0"},
        children=[
            de.EmailContainer([
                de.EmailSection(
                    style={
                        "backgroundColor": "#ffffff",
                        "borderRadius": "8px",
                        "padding": "24px",
                    },
                    children=[
                        de.EmailHeading("Two columns", as_="h3"),
                        de.EmailRow([
                            de.EmailColumn(
                                style={"width": "50%", **CELL},
                                children=[
                                    de.EmailText(
                                        "Left column — rows and columns render "
                                        "as real HTML tables, the only layout "
                                        "primitive every email client supports."
                                    )
                                ],
                            ),
                            de.EmailColumn(
                                style={"width": "50%", **CELL},
                                children=[
                                    de.EmailText(
                                        "Right column — set widths with "
                                        "percentage styles on each column."
                                    )
                                ],
                            ),
                        ]),
                        de.EmailDivider(style={"margin": "16px 0"}),
                        de.EmailHeading("70 / 30 split", as_="h3"),
                        de.EmailRow([
                            de.EmailColumn(
                                style={"width": "70%", **CELL},
                                children=[de.EmailText("Product name")],
                            ),
                            de.EmailColumn(
                                style={"width": "30%", "textAlign": "right", **CELL},
                                children=[de.EmailText("$99.00")],
                            ),
                        ]),
                    ],
                )
            ])
        ],
    )
])
