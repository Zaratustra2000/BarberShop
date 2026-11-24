"""Controllers do barbeiro (US3, US4 e agenda da US5)."""
from flask import Blueprint, redirect, render_template, request, url_for

from app.formatos import ler_data_hora, ler_inteiro, reais_para_centavos
from app.routes.sessao import container, requer_papel, usuario_id

bp = Blueprint("barbeiro", __name__, url_prefix="/barbeiro")


@bp.get("")
@requer_papel("barbeiro")
def painel():
    c = container()
    return render_template(
        "barbeiro/painel.html",
        servicos=c.consultar_servicos_do_barbeiro.executar(usuario_id()),
        agenda=c.consultar_agenda_do_barbeiro.executar(usuario_id()))


@bp.post("/servicos")
@requer_papel("barbeiro")
def cadastrar_servico():
    form = request.form
    container().cadastrar_servico.executar(
        barbeiro_id=usuario_id(), nome=form.get("nome", ""),
        preco_centavos=reais_para_centavos(form.get("preco", "")),
        duracao_minutos=ler_inteiro(form.get("duracao_minutos"), "duração"))
    return redirect(url_for("barbeiro.painel"))


@bp.get("/busca")
@requer_papel("barbeiro")
def busca():
    bairro = request.args.get("bairro", "").strip()
    ofertas = (container().buscar_cadeiras_ociosas.executar(bairro)
               if bairro else [])
    marcadores = {o.barbearia.id: dict(lat=o.barbearia.latitude,
                                       lng=o.barbearia.longitude,
                                       titulo=o.barbearia.nome,
                                       detalhe=o.barbearia.endereco)
                  for o in ofertas}
    return render_template("barbeiro/busca.html", bairro=bairro,
                           ofertas=ofertas,
                           marcadores=list(marcadores.values()))


@bp.post("/blocos")
@requer_papel("barbeiro")
def reservar_bloco():
    form = request.form
    container().reservar_bloco_de_horario.executar(
        barbeiro_id=usuario_id(), barbearia_id=form.get("barbearia_id", ""),
        horario_ocioso_id=form.get("horario_ocioso_id", ""),
        inicio=ler_data_hora(form.get("inicio")),
        fim=ler_data_hora(form.get("fim")))
    return redirect(url_for("barbeiro.painel"))
