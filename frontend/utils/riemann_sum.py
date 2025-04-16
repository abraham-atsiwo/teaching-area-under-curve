import numpy as np
import pandas as pd

import plotly.graph_objects as go
from dash import dcc
import dash_ag_grid as dag 
import dash.html as html 


def create_riemann_dataframe(
    exact_areas, left_areas, right_areas, midpoint_areas, n_values
):
    """
    Creates a DataFrame from lists of Riemann sum results.

    Args:
        exact_areas: List of exact areas (repeated for each n)
        left_areas: List of left Riemann sums
        right_areas: List of right Riemann sums
        midpoint_areas: List of midpoint sums
        n_values: List of interval counts

    Returns:
        pd.DataFrame: Formatted comparison table
    """
    data = {
        "n": n_values,
        "exact": [f"{x:.4f}" for x in exact_areas],
        "left": [f"{x:.4f}" for x in left_areas],
        "right": [f"{x:.4f}" for x in right_areas],
        "midpoint": [f"{x:.4f}" for x in midpoint_areas],
    }

    return pd.DataFrame(data)

def create_riemann_grid(df):
    """
    Creates an AG Grid component with pagination (10 rows per page).
    
    Args:
        df: pandas DataFrame with Riemann sum results
        
    Returns:
        html.Div: Contains the paginated AG Grid and summary
    """
    return html.Div(
        style={"width": "100%", "overflowX": "auto"},
        children=[
            dag.AgGrid(
                id="riemann-sum-grid",
                rowData=df.to_dict("records"),
                columnDefs=[
                    {"headerName": "Intervals (n)", "field": "n", "width": 100, "suppressSizeToFit": True},
                    {"headerName": "Exact Area", "field": "exact", "width": 120, "suppressSizeToFit": True},
                    {"headerName": "Left Sum", "field": "left", "width": 120, "suppressSizeToFit": True},
                    {"headerName": "Right Sum", "field": "right", "width": 120, "suppressSizeToFit": True},
                    {"headerName": "Midpoint Sum", "field": "midpoint", "width": 140, "suppressSizeToFit": True},
                ],
                defaultColDef={
                    "resizable": True,
                    "sortable": True,
                    "filter": False,
                    "suppressSizeToFit": False
                },
                dashGridOptions={
                    "pagination": True,
                    "paginationPageSize": 10,
                    "animateRows": True,
                    "headerHeight": 40,
                    "rowHeight": 40,
                    "domLayout": "autoHeight",
                    "suppressCellFocus": True,
                    "onGridReady": {"function": "params.api.sizeColumnsToFit()"},
                    "onGridSizeChanged": {"function": "params.api.sizeColumnsToFit()"}
                },
                style={
                    "width": "100%",
                    "height": "auto",
                    "minHeight": "300px"  # Fixed minimum height for pagination controls
                },
                className="ag-theme-alpine",
            ),
            html.Div(
                [
                    html.Small(
                        [
                            html.Strong("Summary:"),
                            f" Showing {min(10, len(df))} of {len(df)} total interval sizes",
                        ],
                        className="text-muted",
                    )
                ],
                className="mt-2",
            ),
        ]
    )

def plot_riemann(x, y, method, start, end, func):
    # Generate fine grid for smooth true function curve
    x_fine = np.linspace(start, end, 200)
    y_fine = func(x_fine)

    # Create figure
    fig = go.Figure()

    # Add true function trace
    fig.add_trace(
        go.Scatter(
            x=x_fine,
            y=y_fine,
            mode="lines",
            name="True Function",
            line=dict(color="blue"),
        )
    )

    # Calculate rectangle parameters based on method
    dx = x[1] - x[0]

    if method == "left":
        x_rect = x[:-1]
        y_rect = y[:-1]
        color = "red"
        name = "Left Riemann Sum"
    elif method == "right":
        # Correct right endpoint implementation - rectangles should start at x[i] and use y[i+1]
        x_rect = x[:-1]
        y_rect = y[1:]
        color = "green"
        name = "Right Riemann Sum"
    elif method == "midpoint":
        x_rect = (x[:-1] + x[1:]) / 2
        y_rect = (y[:-1] + y[1:]) / 2  # Approximate midpoint height
        color = "purple"
        name = "Midpoint Riemann Sum"

    # Add rectangles (only show one entry in legend)
    show_in_legend = True
    for i in range(len(x_rect)):
        fig.add_trace(
            go.Scatter(
                x=[x_rect[i], x_rect[i], x_rect[i] + dx, x_rect[i] + dx, x_rect[i]],
                y=[0, y_rect[i], y_rect[i], 0, 0],
                fill="toself",
                mode="lines",
                name=name if show_in_legend else "",
                fillcolor=color,
                opacity=0.4,
                line=dict(width=0),
                showlegend=show_in_legend,
            )
        )
        show_in_legend = False  # Only show first rectangle in legend

    # Add data points
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name="Data Points",
            marker=dict(color="black", size=8),
        )
    )

    # Update layout
    fig.update_layout(
        title=f"{name} Approximation",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        hovermode="closest",
        legend=dict(itemsizing="constant"),  # Makes legend items uniform size
    )

    return dcc.Graph(figure=fig, style={"width": "100%"})


