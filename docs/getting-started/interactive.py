import dash_email as de
import dash_mantine_components as dmc
from dash import Input, Output, callback

component = dmc.Stack([
    dmc.TextInput(
        id="gs-headline-input",
        label="Headline",
        value="Hello from Dash Email",
        maw=400,
    ),
    de.Email([
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "padding": "24px 0"},
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
                                "Hello from Dash Email",
                                id="gs-headline-output",
                                as_="h2",
                            ),
                            de.EmailText(
                                "Email components are regular Dash components — "
                                "drive them with callbacks like anything else."
                            ),
                        ],
                    )
                ])
            ],
        )
    ]),
], gap="md")


@callback(
    Output("gs-headline-output", "children"),
    Input("gs-headline-input", "value"),
)
def update_headline(value):
    return value or "Hello from Dash Email"
