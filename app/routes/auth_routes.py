from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from app.routes.sessao import container, entrar

bp = Blueprint("auth", __name__)

PAINEL_DA_PERSONA = {
    "dono": "dono.painel",
    "barbeiro": "barbeiro.painel",
    "cliente": "cliente.painel",
}


@bp.get("/")
def inicio():
    papel = session.get("papel")
    if papel in PAINEL_DA_PERSONA:
        return redirect(url_for(PAINEL_DA_PERSONA[papel]))
    return render_template("inicio.html")


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    container().cadastrar_usuario.executar(
        nome=request.form.get("nome", ""),
        email=request.form.get("email", ""),
        senha=request.form.get("senha", ""),
        papel=request.form.get("papel", ""))
    return redirect(url_for("auth.login", cadastrado=1))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html",
                               cadastrado=request.args.get("cadastrado"))
    usuario = container().autenticar_usuario.executar(
        email=request.form.get("email", ""),
        senha=request.form.get("senha", ""))
    entrar(usuario)
    return redirect(url_for(PAINEL_DA_PERSONA[usuario.papel.value]))


@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.inicio"))
