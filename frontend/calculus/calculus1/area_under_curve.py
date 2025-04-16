import dash.html as html
import dash_bootstrap_components as dbc


def sidebar():
    return html.Div(
        children=[],
        className="sidebar",
        style={
            "display": "flex",
            "flexDirection": "column",
            "rowGap": "10px",
            "minHeight": "20px",
            "borderStyle": "solid",
        },
    )


def body():
    return html.Div(
        children=[],
        className="sidebar",
        style={
            "display": "flex",
            "flexDirection": "column",
            "rowGap": "10px",
            "minHeight": "20px",
            "borderStyle": "solid",
        },
    )


def sidebar_body():
    return html.Div(
        children=[sidebar(), body()],
        className="sidebar-body",
        style={"display": "flex", "width": "100%"},
    )
