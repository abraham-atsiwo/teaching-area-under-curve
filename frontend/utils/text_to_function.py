from sympy import symbols, lambdify, exp as sympy_exp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication,
    convert_xor
)
import numpy as np

def text_to_function(expr_str):
    """Convert math string to executable function with accurate evaluation"""
    try:
        # Extract RHS if equation format is used
        rhs = expr_str.split('=')[1].strip() if '=' in expr_str else expr_str
        
        # Pre-process the expression
        rhs = rhs.replace('^', '**')  # Convert all ^ to **
        rhs = rhs.replace('e**x', 'exp(x)')  # Handle exponential notation
        
        # Configure parsing rules
        transformations = (
            standard_transformations +
            (implicit_multiplication,  # Handles 2x → 2*x
             convert_xor)             # Additional ^ to ** conversion
        )
        
        # Parse the expression
        x = symbols('x')
        expr = parse_expr(rhs, transformations=transformations)
        
        # Create numeric function with numpy
        numpy_func = lambdify(x, expr, modules=['numpy'])
        
        def evaluator(x_val):
            try:
                # Handle both scalar and array inputs
                x_array = np.array(x_val, dtype=float)
                result = numpy_func(x_array)
                
                # Return appropriate type
                if isinstance(x_val, (list, np.ndarray)):
                    return result.astype(float)
                return float(result)
            
            except Exception as e:
                raise ValueError(f"Evaluation failed at x={x_val}: {str(e)}")
        
        return evaluator
    
    except Exception as e:
        raise ValueError(f"Parsing error: {str(e)}")

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import inspect
import re

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def func_to_latex(func):
    """Convert a Python function to LaTeX notation"""
    # Get function source code
    source = inspect.getsource(func).strip()
    
    # Extract the return expression using regex
    match = re.search(r'return\s+(.+)\s*$', source, re.MULTILINE)
    if not match:
        return r'\text{Unknown function}'
    
    expression = match.group(1)
    
    # Convert Python operators to LaTeX
    latex_expr = (
        expression
        .replace('**', '^')       # Exponents
        .replace('*', r' \cdot ')  # Multiplication
        .replace('np.', '')        # Numpy functions
        .replace('math.', '')      # Math module functions
        .replace('sqrt', r'\sqrt')
        .replace('sin', r'\sin')
        .replace('cos', r'\cos')
        .replace('tan', r'\tan')
        .replace('exp', r'\exp')
        .replace('log', r'\log')
    )
    
    return rf'\text{{conv_func}}(x) = {latex_expr}'