from dash import Dash
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import dash.html as html
import dash.dcc as dcc
import os 


from frontend import navbar, mainbody
from backend import navbar_callback

app = Dash(
    __name__,
    title="Interactive Mathematics Teaching",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server = app.server 


# def main_layout(app: Dash) -> Dash:
#     app.layout = html.Div(
#         children=[
#             html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_SVG"),
#             html.Div(children=[navbar(app), mainbody(app)], className="container")
#         ],
#         className="main-container",
#         id="main_container",
#     )
#     return app


# def main_callback(app):
#     navbar_callback(app)


# def main(app, port):
#     main_layout(app)
#     main_callback(app)
#     return app.run(debug=False, port=port)


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8050))
#     # print(port)
#     main(app=app, port=port)



app.layout = html.Div(
    children=[
        html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_SVG"),
        html.Div(children=[navbar(app), mainbody(app)], className="container")
    ],
    className="main-container",
    id="main_container",
)

navbar_callback(app)






if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(port=port, debug=False)
    
