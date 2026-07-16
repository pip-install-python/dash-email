import dash_email as de

ROW_STYLE = {"padding": "6px 0"}

component = de.Email([
    de.EmailPreview("Your order #12345 has been confirmed"),
    de.EmailBody(
        style={"backgroundColor": "#f6f9fc", "padding": "24px 0"},
        children=[
            de.EmailContainer([
                de.EmailSection(
                    style={
                        "backgroundColor": "#ffffff",
                        "padding": "40px",
                        "borderRadius": "8px",
                    },
                    children=[
                        de.EmailHeading("Order Confirmed! 🎉", as_="h1"),
                        de.EmailText(
                            "Thank you for your purchase. Here's a summary of "
                            "your order #12345."
                        ),
                        de.EmailDivider(),
                        de.EmailRow([
                            de.EmailColumn(
                                style={"width": "70%", **ROW_STYLE},
                                children=[de.EmailText("Mechanical Keyboard")],
                            ),
                            de.EmailColumn(
                                style={"width": "30%", "textAlign": "right", **ROW_STYLE},
                                children=[de.EmailText("$99.00")],
                            ),
                        ]),
                        de.EmailRow([
                            de.EmailColumn(
                                style={"width": "70%", **ROW_STYLE},
                                children=[de.EmailText("USB-C Cable")],
                            ),
                            de.EmailColumn(
                                style={"width": "30%", "textAlign": "right", **ROW_STYLE},
                                children=[de.EmailText("$12.00")],
                            ),
                        ]),
                        de.EmailDivider(),
                        de.EmailRow([
                            de.EmailColumn(
                                style={"width": "70%", **ROW_STYLE},
                                children=[
                                    de.EmailText(
                                        "Total",
                                        style={"fontWeight": "bold"},
                                    )
                                ],
                            ),
                            de.EmailColumn(
                                style={"width": "30%", "textAlign": "right", **ROW_STYLE},
                                children=[
                                    de.EmailText(
                                        "$111.00",
                                        style={"fontWeight": "bold"},
                                    )
                                ],
                            ),
                        ]),
                        de.EmailButton(
                            "Track Your Order",
                            href="https://example.com/track",
                            style={
                                "backgroundColor": "#28a745",
                                "color": "#ffffff",
                                "padding": "14px 28px",
                                "borderRadius": "4px",
                                "marginTop": "16px",
                            },
                        ),
                    ],
                )
            ])
        ],
    ),
])
