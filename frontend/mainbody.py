from typing import List

import sympy as sp
import numpy as np
import pandas as pd
from scipy.integrate import quad
from sympy.parsing.sympy_parser import parse_expr

import dash.html as html
from dash import Input, Output, State, callback, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from .utils.text_to_function import text_to_function, func_to_latex
from .utils.riemann_sum import (
    plot_riemann,
    create_riemann_dataframe,
    create_riemann_grid,
)


def generate_points(a, b, n):
    return np.linspace(a, b, num=n + 1)


def approximate_area(x, y, method):
    """
    Approximates the area under a curve using left, right, or midpoint Riemann sums.

    Parameters:
        x (array-like): Array of x-values (must be equally spaced).
        y (array-like): Array of y-values corresponding to x.
        method (str): 'left', 'right', or 'midpoint'.

    Returns:
        float: Approximated area.
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")
    if method not in ["left", "right", "midpoint"]:
        raise ValueError("Method must be 'left', 'right', or 'midpoint'.")

    dx = x[1] - x[0]  # Assuming uniform spacing
    n = len(x) - 1  # Number of intervals

    if method == "left":
        areas = [y[i] * dx for i in range(n)]
    elif method == "right":
        areas = [y[i + 1] * dx for i in range(n)]
    elif method == "midpoint":
        areas = [((y[i] + y[i + 1]) / 2) * dx for i in range(n)]

    return sum(areas)


def sidebar(chidren: List = 1):
    if not chidren:
        chidren = []
    else:
        textarea = html.Div(
            [
                dbc.Label("enter function:", html_for="comment-box", className="mb-2"),
                dbc.Textarea(
                    id="function_box",
                    placeholder="enter your function here. Example: y = x^2",
                    style={"width": "100%", "maxHeight": "50px"},
                ),
            ],
            style={"width": "100%"},
        )

        start_num = html.Div(
            [
                dbc.Label("start", html_for="start-input", className="me-2 mb-0"),
                dbc.Input(
                    id="start_input",
                    type="number",
                    placeholder="enter the left endpoint",
                    style={"width": "100%"},
                ),
            ],
            className="d-flex align-items-center",
        )

        end_num = html.Div(
            [
                dbc.Label("end:", html_for="end-input", className="me-2 mb-0"),
                dbc.Input(
                    id="end_input",
                    type="number",
                    placeholder="enter the right endpoint",
                    style={"width": "100%"},
                ),
            ],
            className="d-flex align-items-center",
        )
        num_rect = html.Div(
            [
                dbc.Label("nrec:", html_for="rect-input", className="me-2 mb-0"),
                dbc.Input(
                    id="num_rectangle",
                    type="number",
                    placeholder="enter the number of rectangles",
                    style={"width": "100%"},
                ),
            ],
            className="d-flex align-items-center",
        )

        endpoint_type = html.Div(
            [
                dbc.Label("sample input:", html_for="sample-input", className="me-2"),
                dbc.Select(
                    id="endpoint_type",
                    options=[
                        {"label": "left", "value": "left"},
                        {"label": "right", "value": "right"},
                        {"label": "midpoint", "value": "midpoint"},
                        # {"label": "all", "value": "all"},
                    ],
                    style={"width": "100%"},
                    value="midpoint",
                ),
            ],
            className="d-flex align-items-center",
        )
        chidren = [
            textarea,
            html.Hr(),
            start_num,
            end_num,
            html.Hr(),
            num_rect,
            endpoint_type,
            html.Hr(),
            dbc.Button("GET RESULT", color="success", id="get_result", n_clicks=0),
            html.Div(
                children=[],
                id="error",
                style={
                    "minHeight": "40px",
                    "width": "100%",
                    "backgroundColor": "red",
                    "fontWeight": "bold",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                },
            ),
        ]

    return html.Div(children=chidren, id="sidebar", className="sidebar body-item")


def content(children: List = None):
    if not children:
        children = []
    return html.Div(children=[], className="content body-item", id="content")


def mainbody(app):
    return html.Div(
        children=[sidebar(), content()],
        className="mainbody-container",
        id="mainbody_container",
    )


@callback(
    Output(component_id="content", component_property="children"),
    Output(component_id="error", component_property="children"),
    State(component_id="function_box", component_property="value"),
    State(component_id="start_input", component_property="value"),
    State(component_id="end_input", component_property="value"),
    State(component_id="num_rectangle", component_property="value"),
    State(component_id="endpoint_type", component_property="value"),
    Input(component_id="get_result", component_property="n_clicks"),
)
def main(func, start, end, num, endpoint, n_clicks):
    remain = ""
    text = ""
    body = ""
    if n_clicks > 0:
        if func is None:
            text = "enter function"
            remain = "cannot be empty or null!"
        elif start is None:
            text = "left endpoint"
            remain = "cannot be empty or null!"
        elif end is None:
            text = "right endpoint"
            remain = "cannot be empty or null!"
        elif num is None:
            text = " number of rectangles"
            remain = "cannot be empty or null!"
        elif endpoint is None:
            text = "endpoint"
            remain = "cannot be empty or null!"

        elif start >= end:
            text = "start must be"
            remain = "less than end"

        elif num <= 0:
            text = "number of rectangles"
            remain = "must be positive"

        else:
            conv_func = text_to_function(func)
            x = generate_points(a=start, b=end, n=num)
            height = conv_func(x)
            area = approximate_area(x=x, y=height, method=endpoint)
            # plot graph
            plot = plot_riemann(
                x=x, y=height, method=endpoint, start=start, end=end, func=conv_func
            )

            # compare result
            nrange = [num] + [n for n in range(1, 5000, 10)]

            def generate_point_based_n(nlist, method):
                def inner():
                    for n in nlist:
                        x = generate_points(a=start, b=end, n=n)
                        height = conv_func(x)
                        yield approximate_area(x=x, y=height, method=method)

                return list(inner())

            left_area = generate_point_based_n(nlist=nrange, method="left")
            right_area = generate_point_based_n(nlist=nrange, method="right")
            midpoint_area = generate_point_based_n(nlist=nrange, method="midpoint")
            # calculate exact area
            e_area = quad(conv_func, start, end)[0]
            exact = [e_area] * len(left_area)
            # table of value
            table = create_riemann_dataframe(
                exact_areas=exact,
                midpoint_areas=midpoint_area,
                right_areas=right_area,
                left_areas=left_area,
                n_values=nrange,
            )

            table = create_riemann_grid(table)
            body = html.Div(
                children=[plot, html.Hr(), table],
                style={"width": "100%", "display": "flex", "flexDirection": "column"},
            )
            if "=" in func:
                text = func
            else:
                text = "y = " + func

        return [body, f"{text} {remain}"]

    return ["", ""]
