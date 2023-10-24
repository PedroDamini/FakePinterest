from flask import render_template, url_for
from fake_pinterest import app
from flask_login import login_required
from fake_pinterest.forms import FormCriarConta, FormLogin

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    return render_template("homepage.html", form=formlogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    formcriarconta = FormCriarConta()
    return render_template("criar_conta.html", form=formcriarconta)

@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)
