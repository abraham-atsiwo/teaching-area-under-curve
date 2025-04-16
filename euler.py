import streamlit as st 
from frontend.utils.text_to_function import text_to_function


def euler_method(a, b, h, func, y0):
    """
    Solve an ODE using Euler's method.
    
    Parameters:
    a (float): Initial x value
    b (float): Final x value
    h (float): Step size
    func (function): The derivative function dy/dx = func(x, y)
    y0 (float): Initial condition y(a)
    
    Returns:
    tuple: (x_values, y_values) for plotting
    """
    x_values = []
    y_values = []
    
    # Initialize variables
    x = a
    y = y0
    
    # Store initial values
    x_values.append(x)
    y_values.append(y)
    
    # Perform Euler's method
    while x < b:
        y = y + h * func(x, y)  # Euler's formula
        x = x + h
        
        # Store current values
        x_values.append(x)
        y_values.append(y)
    
    return x_values, y_values

with st.sidebar:
    func = st.text_area(label="Enter Function")
    a = st.number_input(label="starting x-value")
    b = st.number_input(label="Right Endpoint")
    y = st.number_input(label="Starting y")
    h = st.number_input("Step Size")

#body 
if func and a and b and y and y:
    conv_func = text_to_function(expr_str=func)
    result = euler_method(a=a, b=b, h=h, y0=y)
    print(result)


