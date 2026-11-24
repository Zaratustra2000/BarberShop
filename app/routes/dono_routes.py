"""Controllers do dono (US2): traduzem formulários em chamadas de casos de
uso e o resultado em HTML. Nenhuma regra de negócio mora aqui."""
from flask import Blueprint, redirect, render_template, request, url_for

from app.formatos import (ler_data_hora, ler_decimal, ler_inteiro,
                          reais_para_centavos)
from app.routes.sessao import container, requer_papel, usuario_id

bp = Blueprint("dono", __name__, url_prefix="/dono")


@bp.get("")
@requer_papel("dono")
def painel():
    barbearias = container().consultar_barbearias_do_dono.executar(
        usuario_id())
    return render_template("dono/painel.html", barbearias=barbearias)


@bp.get("/barbearias/nova")
@requer_papel("dono")
def nova_barbearia():
    return render_template("dono/nova_barbearia.html")


@bp.post("/barbearias")
@requer_papel("dono")
def cadastrar_barbearia():
    form = request.form
    barbearia = container().cadastrar_barbearia.executar(
        dono_id=usuario_id(), nome=form.get("nome", ""),
        endereco=form.get("endereco", ""), bairro=form.get("bairro", ""),
        latitude=ler_decimal(form.get("latitude"), "latitude"),
        longitude=ler_decimal(form.get("longitude"), "longitude"),
        regras=form.get("regras", ""),
        quantidade_de_cadeiras=ler_inteiro(
            form.get("quantidade_de_cadeiras"), "quantidade de cadeiras"))
    return redirect(url_for("dono.barbearia", barbearia_id=barbearia.id))


@bp.get("/barbearias/<barbearia_id>")
@requer_papel("dono")
def barbearia(barbearia_id):
    barbearia = container().consultar_barbearias_do_dono.uma(
        usuario_id(), barbearia_id)
    return render_template("dono/barbearia.html", barbearia=barbearia,
                           nome_da_cadeira={c.id: c.nome
                                            for c in barbearia.cadeiras})


@bp.post("/barbearias/<barbearia_id>/horarios")
@requer_papel("dono")
def publicar_horario(barbearia_id):
    form = request.form
    container().publicar_horario_ocioso.executar(
        dono_id=usuario_id(), barbearia_id=barbearia_id,
        cadeira_id=form.get("cadeira_id", ""),
        inicio=ler_data_hora(form.get("inicio")),
        fim=ler_data_hora(form.get("fim")),
        preco_por_hora_centavos=reais_para_centavos(
            form.get("preco_por_hora", "")))
    return redirect(url_for("dono.barbearia", barbearia_id=barbearia_id))
