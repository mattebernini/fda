from flask import Blueprint, render_template, request, jsonify
import website.utility as uty

teoria = Blueprint('teoria', __name__)

@teoria.route("/teoria", methods=['GET', 'POST'])
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

@teoria.route('/ajax/stability', methods=['POST'])
def stability():
    fdt = request.form['fdt']
    return jsonify(uty.print_result("stability", fdt))