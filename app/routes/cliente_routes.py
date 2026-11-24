from flask import Blueprint, render_template

from app.routes.sessao import requer_papel

bp = Blueprint("cliente", __name__, url_prefix="/cliente")


@bp.get("")
@requer_papel("cliente")
def painel():
    return render_template("cliente/painel.html")
