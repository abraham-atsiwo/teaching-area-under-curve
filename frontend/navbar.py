import dash.html as html
import dash_bootstrap_components as dbc

from utils.subjects import SUBJECT 


def navbar(app):
    logo = html.Div("ITeach", className="navbar-item")
    subject = html.Div(
        [
            dbc.Label("Subject:", html_for="subject-dropdown", className="me-2", style={"display": "none"}),
            dbc.Select(
                id="subject_dropdown",
                options=[
                    {"label": course, "value": course} for course in SUBJECT
                ],
                style={"maxWidth": "300px", "marginRight": "10px", "display": "none"},
            ),
        ],
        className="d-flex align-items-center",
    )
    topic = html.Div(
        [
            dbc.Label("Topic:", html_for="subject-dropdown", className="me-2",  style={"display": "none"}),
            dbc.Select(
                id="topic_dropdown",
                options=[],
                style={"maxWidth": "300px",  "display": "none"},
            ),
        ],
        className="d-flex align-items-center"
    )
    subject_topic = html.Div(children=[subject, topic], className="navbar-item", style={"diplay": "none"})
    switch = html.Div(
        [
            dbc.Checklist(
                options=[{"label": " Dark Mode", "value": "dark"}],
                value=["dark"],
                id="toggle-switch",
                switch=True,
                inline=True,
            )
        ],
        className="navbar-item", style={"diplay": "none"}
    )
    return html.Nav(
        children=[logo, subject_topic, switch], className="navbar-container"
    )
