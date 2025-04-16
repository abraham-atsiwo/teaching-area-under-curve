from sympy import symbols, lambdify, sympify, latex
from sympy.parsing.sympy_parser import parse_expr


def text_to_function_safe(expression):
    """Safely convert text to Python function using sympy"""
    x = symbols("x")
    expr = parse_expr(expression.replace("^", "**"))
    return lambdify(x, expr, modules=["numpy"])


# # Usage
# f = text_to_function_safe("2*x^2 + sin(x) + exp(x)")
# print(f(1))  # Output: 5.559752813


def text_to_latex(text):
    try:
        expr = sympify(text.replace("^", "**"))  # Handle ^ for exponents
        return latex(expr)
    except:
        return text  # Fallback for invalid input


# print(text_to_latex("2*x^2 + sin(x) + e^x"))  # Output: 2x
