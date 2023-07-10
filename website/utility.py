import sympy
import warnings, os

sympy.init_printing()
warnings.filterwarnings('ignore')
t, s = sympy.symbols('t s')

def L(f):
    return sympy.laplace_transform(f, t, s, noconds=True)

def invL(F):
    return sympy.inverse_laplace_transform(F, s, t)

def laplace(f):
    f = sympy.sympify(f)  # Convert the string to a sympy expression
    if isinstance(f, sympy.Expr) and f.has(t):
        return sympy.laplace_transform(f, t, s, noconds=True)
    elif isinstance(f, sympy.Expr) and f.has(s):
        return sympy.inverse_laplace_transform(f, s, t)
    else:
        raise ValueError("Invalid input")
    
def plot(arg, f):
    os.system(f"echo '{f}' | octave website/static/teoria/octave/{arg}.m")

def print_result(arg, f):
    os.system(f"echo '{f}' | octave website/static/teoria/octave/{arg}.m")
    file = open("website/static/teoria/files/result.txt", "r")
    return file.read()