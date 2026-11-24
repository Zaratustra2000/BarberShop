from flask import Blueprint, render_template

from app.routes.sessao import requer_papel

bp = Blueprint("barbeiro", __name__, url_prefix="/barbeiro")


@bp.get("")
@requer_papel("barbeiro")
def painel():
    return render_template("barbeiro/painel.html")
