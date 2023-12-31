from flask import Blueprint, render_template, request, jsonify
import website.utility as uty

teoria = Blueprint('teoria', __name__)

@teoria.route("/", methods=['GET', 'POST'])
def teoria_home():
    return render_template("teoria.html")
                           
@teoria.route('/ajax/laplace', methods=['POST'])
def laplace():
    fdt = request.form['fdt']
    transformed_fdt = uty.laplace(fdt)
    print(transformed_fdt)
    return jsonify(str(transformed_fdt))
                           
@teoria.route('/ajax/bode', methods=['POST'])
def bode():
    fdt = request.form['fdt']
    uty.plot("bode", fdt)
    return jsonify("ok")

@teoria.route('/ajax/nyquist', methods=['POST'])
def nyquist():
    fdt = request.form['fdt']
    uty.plot("nyquist", fdt)
    return jsonify("ok")

@teoria.route('/ajax/rlocus', methods=['POST'])
def rlocus():
    fdt = request.form['fdt']
    uty.plot("rlocus", fdt)
    return jsonify("ok")

@teoria.route('/ajax/step', methods=['POST'])
def step():
    fdt = request.form['fdt']
    xi = fdt.split(",")[0]
    wn = fdt.split(",")[1]
    uty.sys_2nd_order(float(xi), float(wn))
    return jsonify("ok")

@teoria.route('/ajax/matrix', methods=['POST'])
def matrix():
    A = request.form['A']
    B = request.form['B']
    C = request.form['C']
    D = request.form['D']
    return jsonify(uty.result_matrici(A,B,C,D))

@teoria.route('/ajax/valore_finale', methods=['POST'])
def valore_finale():
    fdt = request.form['fdt']
    return jsonify(uty.calculate_final_value(fdt))

@teoria.route('/ajax/errore', methods=['POST'])
def errore():
    fdt = request.form['fdt']
    return jsonify(uty.calculate_ss_error(fdt))
