from dash import Dash, html, dcc, Input, Output


def currency_bar(cur):
    return html.Div(className="currency_box", children=[
        dcc.Dropdown(
        id="check_you_currency",

        value="BRL",
        options=("USD", "BRL"),
        clearable=False,
        searchable=True
        )
    ])