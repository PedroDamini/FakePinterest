from flask import render_template, url_for, redirect
from fake_pinterest import app, database, bcrypt
from fake_pinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from fake_pinterest.forms import FormCriarConta, FormLogin, FormFoto
from werkzeug.utils import secure_filename
import os

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", username_usuario=usuario.username))
        
    return render_template("homepage.html", form=form_login)

@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        if Usuario.query.filter_by(email=form_criar_conta.email.data).first():
            return "Esse usuario ja existe"
        else:
            senha = bcrypt.generate_password_hash(form_criar_conta.senha.data)
            usuario = Usuario(username=form_criar_conta.username.data, 
                                senha=senha, 
                                email=form_criar_conta.email.data)
            database.session.add(usuario)
            database.session.commit()
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", username_usuario=usuario.username))

    return render_template("criar_conta.html", form=form_criar_conta)

@app.route("/perfil/<username_usuario>", methods=["GET", "POST"])
@login_required
def perfil(username_usuario):
    if username_usuario == current_user.username:
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config["UPLOAD_FOLDER"],
                                nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.filter_by(username=username_usuario).first()
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
