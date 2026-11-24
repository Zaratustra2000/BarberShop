"""Controllers do barbeiro (US3, US4 e agenda da US5)."""
from flask import Blueprint, redirect, render_template, request, url_for

from app.formatos import ler_inteiro, reais_para_centavos
from app.routes.sessao import container, requer_papel, usuario_id

bp = Blueprint("barbeiro", __name__, url_prefix="/barbeiro")


@bp.get("")
@requer_papel("barbeiro")
def painel():
    servicos = container().consultar_servicos_do_barbeiro.executar(
        usuario_id())
    return render_template("barbeiro/painel.html", servicos=servicos)


@bp.post("/servicos")
@requer_papel("barbeiro")
def cadastrar_servico():
    form = request.form
    container().cadastrar_servico.executar(
        barbeiro_id=usuario_id(), nome=form.get("nome", ""),
        preco_centavos=reais_para_centavos(form.get("preco", "")),
        duracao_minutos=ler_inteiro(form.get("duracao_minutos"), "duração"))
    return redirect(url_for("barbeiro.painel"))
