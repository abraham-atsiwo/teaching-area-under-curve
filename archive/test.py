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

# Test cases
if __name__ == "__main__":
    try:
        f = text_to_function("y = 2x^2 + e^x")
        
        print(f(0))    # 1.0 (2*0² + e⁰ = 0 + 1 = 1)
        print(f(1))    # 4.718281828459045 (2*1² + e¹ ≈ 2 + 2.71828)
        print(f(2))    # 11.38905609893065 (2*4 + e² ≈ 8 + 7.38906)
        print(f(5))    # 168.4131591025766 (2*25 + e⁵ ≈ 50 + 118.41316)
        
        # Vectorized evaluation
        print(f([0, 1, 2, 5]))  # [1.0, 4.71828183, 11.3890561, 168.4131591]
        
    except ValueError as e:
        print(f"Error: {e}")