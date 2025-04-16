from dash import Input, Output
from dash.exceptions import PreventUpdate

from utils.subjects import SUBJECT 


def toogle_background_callback(app):
    @app.callback(
        Output(component_id="main_container", component_property="style"),
        Input(component_id="toggle-switch", component_property="value"),
    )
    def main(switch):
        if "dark" in switch:
            return {
                "width": "100%",
                "height": "100vh",
                "margin": "0 auto",
                "backgroundColor": "black",
                "color": "white",
            }
        return {
            "width": "100%",
            "height": "100vh",
            "margin": "0 auto",
            "backgroundColor": "rgba(255, 255, 255, 0.446)",
            "color": "black",
        }


def subject_callback(app):
    @app.callback(
        Output(component_id="topic_dropdown", component_property="options"),
        Input(component_id="subject_dropdown", component_property="value"),
    )
    def main(subject):
        if not subject:
            return []
        return SUBJECT[subject]



def navbar_callback(app):
    toogle_background_callback(app)
    subject_callback(app)