from flask import Blueprint, render_template

from app.routes.sessao import requer_papel

bp = Blueprint("dono", __name__, url_prefix="/dono")


@bp.get("")
@requer_papel("dono")
def painel():
    return render_template("dono/painel.html", barbearias=[])
