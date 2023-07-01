from flask import Blueprint, render_template, Markup, request
import os, re
import sympy

fda = Blueprint('fda', __name__)

error_output_file = "website/static/fda/error_output.err"


@fda.route("/", methods=['GET', 'POST'])
def input_fda():
    return render_template("fda.html",
                           cosa="in")

def get_results_fdt():
    data_dict = {}
    f = open("website/static/fda/result.txt", "r")
    lines = f.readlines()
    current_key = None
    for line in lines:
        line = line.strip()  
        if line:  
            if line.startswith('[]') or line.startswith("Inf"):
                # Skip the line with '[]'
                continue
            elif re.match(r'^[-+]?\d*\.?\d+(?:\([^\)]+\))?', line):  
                number = line.replace('(', '').replace(')', '') 
                if current_key in data_dict:
                    if not isinstance(data_dict[current_key], list):
                        data_dict[current_key] = [data_dict[current_key]]
                    data_dict[current_key].append(number)
                else:
                    data_dict[current_key] = number
            else:
                current_key = line  
    return data_dict

def invL(F):
    t, s = sympy.symbols('t, s')    
    return sympy.inverse_laplace_transform(F, s, t)


@fda.route("/result_fdt", methods=['GET', 'POST'])
def fda_result_fdt():
    if request.method == 'POST':
        fdt = request.form['transfer_function']
        compensator = request.form['compensator']
        if compensator:
            cosa = "compensator"
            with open('website/static/fda/in_fdt.txt', 'w') as file:
                file.write(f"{fdt}\n")
                file.write(f"{compensator}\n")
            exit_code = os.system(f"octave website/static/fda/compensator.m 2> {error_output_file}")
            ris = get_results_fdt()
        else:
            cosa = "fdt"
            exit_code = os.system(f"echo '"+fdt+f"' | octave website/static/fda/fdt.m 2> {error_output_file}")
            ris = get_results_fdt()
        if exit_code != 0:
        # qualsiasi errore
            cosa = "errore"
            with open(error_output_file, "r") as file:
                error_output = file.read()
            return render_template("fda.html",
                           cosa=cosa,
                           errore = f"Error occurred. Exit code: {exit_code}\n{error_output}"
                           ) 
    # tutto  ok
    return render_template("fda.html",
                           cosa=cosa,
                           transfer_function=fdt, 
                           compensator = compensator,
                           numeric_result = ris
                           )

@fda.route("/result_matrici", methods=['GET', 'POST'])
def fda_result_matrici():
    if request.method == 'POST':
        A_str = request.form['A']
        B_str = request.form['B']
        C_str = request.form['C']
        D_str = request.form['D']
        with open('website/static/fda/in_matrici.txt', 'w') as file:
            file.write(f"{A_str}\n")
            file.write(f"{B_str}\n")
            file.write(f"{C_str}\n")
            file.write(f"{D_str}\n")
        exit_code = os.system("octave website/static/fda/matrici.m")
        f = open("website/static/fda/result.txt", "r")
    return render_template("fda.html",
                           cosa="matrici",
                           ris = f.readlines()
                           )


