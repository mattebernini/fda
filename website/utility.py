import sympy
import numpy as np
import matplotlib.pyplot as plt
import warnings, os
import control
from sympy import symbols, simplify, apart, fraction, Poly
from sympy import limit


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

def sys_2nd_order(xi, wn):
    S = np.exp(-xi*3.14/(np.sqrt(1-xi**2)))
    t_max = 3.14/(wn*np.sqrt(1-xi**2))
    t_s = -1/(xi*wn)*np.log(0.05)
    Tp = 2*3.14/(wn*np.sqrt(1-xi**2))

    time = np.linspace(0,30,100)
    fig = plt.figure(figsize=(15,5))

    y_t = 1 - (1/np.sqrt(1-xi**2)) * np.exp(-xi*wn*time) * np.sin(wn*np.sqrt(1-xi**2)*time+np.arccos(xi))
    plt.plot(time, y_t, linewidth=4)
    plt.plot([t_max, t_max], [y_t[-1], y_t[-1]+S], marker='.', markersize=12)
    plt.text(t_max+0.2, y_t[-1]+S/2, 'S', fontsize=15) 
    plt.plot([t_max, t_max], [0, 1], markersize=12, linestyle='--')
    plt.text(t_max+0.2, 0.0, 't_max', fontsize=15) 
    plt.plot([0, time[-1]], [1-0.05, 1-0.05], linestyle='--', color='k')
    plt.plot([0, time[-1]], [1+0.05, 1+0.05], linestyle='--', color='k')
    plt.plot([t_s, t_s], [0, 1.1], linestyle='--')
    plt.text(t_s+0.2, 0.0, 't_s', fontsize=15) 
    plt.plot([t_max, t_max+Tp], [y_t[-1]+S+0.1, y_t[-1]+S+0.1], 
            marker='.', linestyle='--', color='k', markersize=10)
    plt.plot([t_max+Tp, t_max+Tp], [y_t[-1], y_t[-1]+S+0.1], linestyle='--', color='k')
    plt.text((t_max+t_max+Tp)/2, y_t[-1]+S, 'Tp', fontsize=15)
    fig.legend(['xi:{:.1f}'.format(xi)], loc='upper left')
    plt.title('Step response')
    plt.xlabel('time (s)')
    plt.grid()
    plt.savefig("website/static/teoria/files/step.jpg")

# from a str input i got a transfer function in the s domain
def fdt(f):
    s = symbols('s')
    tf_expr = eval(f)
    num_expr, den_expr = fraction(simplify(apart(tf_expr, s)))
    num_coeffs = Poly(num_expr, s).all_coeffs()
    den_coeffs = Poly(den_expr, s).all_coeffs()

    num_coeffs = [float(coeff) for coeff in num_coeffs]
    den_coeffs = [float(coeff) for coeff in den_coeffs]
    tf = control.TransferFunction(num_coeffs, den_coeffs)
    print(tf)
    return tf

def calculate_final_value(tf_str):
    s = symbols('s')

    tf = eval(f"({tf_str})*s")
    impulse = limit(tf, s, 0)

    tf = eval(tf_str)
    step = limit(tf, s, 0)

    tf = eval(f"({tf_str})/s")
    ramp = limit(tf, s, 0)
    
    return f"impulso -> {impulse}, gradino -> {step}, rampa -> {ramp}"

def calculate_ss_error(tf_str):
    s = symbols('s')

    tf = eval(f"s/(1 + {tf_str})")
    impulse = limit(tf, s, 0)

    tf = eval(f"1/(1 + {tf_str})")
    step = limit(tf, s, 0)

    tf = eval(f"1/(s * (1 + {tf_str}))")
    ramp = limit(tf, s, 0)
    
    return f"impulso -> {impulse}, gradino -> {step}, rampa -> {ramp}"
