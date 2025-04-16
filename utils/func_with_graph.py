import numpy as np
import matplotlib.pyplot as plt


def plot_riemann(x, y, method, start, end, func):
    x_fine = np.linspace(start, end, 200)
    y_fine = func(x_fine)
    plt.figure(figsize=(10, 6))
    plt.plot(x_fine, y_fine, "b-", label="True Function ($y = x^2$)")
    dx = x[1] - x[0]

    if method == "left":
        # Left endpoints: rectangles anchored at left
        plt.bar(
            x[:-1],
            y[:-1],
            width=dx,
            alpha=0.4,
            align="edge",
            color="red",
            label="Left Riemann Sum",
        )
        plt.title("Left-Endpoint Riemann Sum")
    elif method == "right":
        # Right endpoints: rectangles anchored at right
        plt.bar(
            x[1:],
            y[1:],
            width=-dx,
            alpha=0.4,
            align="edge",
            color="green",
            label="Right Riemann Sum",
        )
        plt.title("Right-Endpoint Riemann Sum")
    elif method == "midpoint":
        # Midpoints: rectangles centered on midpoint
        mid_x = (x[:-1] + x[1:]) / 2
        mid_y = (y[:-1] + y[1:]) / 2  # Approximate midpoint height
        plt.bar(
            mid_x,
            mid_y,
            width=dx,
            alpha=0.4,
            color="purple",
            label="Midpoint Riemann Sum",
        )
        plt.title("Midpoint Riemann Sum")

    plt.scatter(x, y, color="black", zorder=5, label="Data Points")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
