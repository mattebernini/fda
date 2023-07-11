import sympy
import numpy as np
import matplotlib.pyplot as plt
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

def sys_2nd_order(xi, wn):
    # Maximum overshoot
    S = np.exp(-xi*3.14/(np.sqrt(1-xi**2)))
    # Time of maximum overshoot
    t_max = 3.14/(wn*np.sqrt(1-xi**2))
    # Settling time within 5%
    t_s = -1/(xi*wn)*np.log(0.05)
    # Period of the oscillations
    Tp = 2*3.14/(wn*np.sqrt(1-xi**2))

    # time vector
    time = np.linspace(0,30,100)
    # create the figure
    fig = plt.figure(figsize=(15,5))

    # overall response y(t)
    y_t = 1 - (1/np.sqrt(1-xi**2)) * np.exp(-xi*wn*time) * np.sin(wn*np.sqrt(1-xi**2)*time+np.arccos(xi))
    plt.plot(time, y_t, linewidth=4)

    # maximum overshoot
    plt.plot([t_max, t_max], [y_t[-1], y_t[-1]+S], marker='.', markersize=12)
    plt.text(t_max+0.2, y_t[-1]+S/2, 'S', fontsize=15) # text box

    # Time of maximum overshoot
    plt.plot([t_max, t_max], [0, 1], markersize=12, linestyle='--')
    plt.text(t_max+0.2, 0.0, 't_max', fontsize=15) # text box

    # Let's also plot +-0.05 boundary lines around y(t)
    plt.plot([0, time[-1]], [1-0.05, 1-0.05], linestyle='--', color='k')
    plt.plot([0, time[-1]], [1+0.05, 1+0.05], linestyle='--', color='k')

    # Settling time within a desired +-0.05 interval
    plt.plot([t_s, t_s], [0, 1.1], linestyle='--')
    plt.text(t_s+0.2, 0.0, 't_s', fontsize=15) # textbox

    # Oscillation period (this is only to show it on the plot)
    plt.plot([t_max, t_max+Tp], [y_t[-1]+S+0.1, y_t[-1]+S+0.1], 
            marker='.', linestyle='--', color='k', markersize=10)
    plt.plot([t_max+Tp, t_max+Tp], [y_t[-1], y_t[-1]+S+0.1], linestyle='--', color='k')
    plt.text((t_max+t_max+Tp)/2, y_t[-1]+S, 'Tp', fontsize=15)

    fig.legend(['xi:{:.1f}'.format(xi)], loc='upper left')

    plt.title('Step response')
    plt.xlabel('time (s)')
    plt.grid()
    plt.savefig("website/static/teoria/files/step.jpg")