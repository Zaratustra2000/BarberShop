"""Controllers do barbeiro (US3, US4 e agenda da US5)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.formatos import ler_data_hora, ler_inteiro, reais_para_centavos
from app.routes.sessao import container, requer_papel, usuario_id
from domain.erros import AcessoNegado, DadosInvalidos, NaoEncontrado
from use_cases.validar_foto_da_barbearia import LIMITE_DE_FOTO

bp = Blueprint("barbeiro", __name__, url_prefix="/barbeiro")


@bp.get("")
@requer_papel("barbeiro")
def painel():
    c = container()
    visao = c.consultar_agenda_do_barbeiro.executar(usuario_id())
    return render_template(
        "barbeiro/painel.html",
        servicos=c.consultar_servicos_do_barbeiro.executar(usuario_id()),
        agenda=visao.agenda.itens, nomes=visao.nomes_dos_clientes)


@bp.get("/perfil")
@requer_papel("barbeiro")
def perfil():
    barbeiro = container().consultar_perfil_do_barbeiro.executar(
        usuario_id()).barbeiro
    return render_template("barbeiro/perfil.html", barbeiro=barbeiro)


@bp.post("/perfil")
@requer_papel("barbeiro")
def editar_perfil():
    container().editar_perfil_do_barbeiro.executar(
        barbeiro_id=usuario_id(),
        nome=request.form.get("nome", ""),
        apresentacao=request.form.get("apresentacao", ""))
    return redirect(url_for("barbeiro.perfil"))


@bp.post("/perfil/foto")
@requer_papel("barbeiro")
def atualizar_foto_do_perfil():
    arquivo = request.files.get("foto")
    if arquivo is None or not arquivo.filename:
        flash("Envie uma imagem JPG, PNG ou WebP.", "erro")
        return redirect(url_for("barbeiro.perfil"))

    conteudo = arquivo.read(LIMITE_DE_FOTO + 1)
    try:
        extensao = container().validar_foto_do_barbeiro.executar(conteudo)
    except DadosInvalidos as erro:
        flash(str(erro), "erro")
        return redirect(url_for("barbeiro.perfil"))

    container().substituir_foto_do_barbeiro.executar(
        barbeiro_id=usuario_id(), conteudo=conteudo, extensao=extensao)
    return redirect(url_for("barbeiro.perfil"))


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
    resultados = container().buscar_cadeiras_ociosas.executar(bairro)
    ofertas = [o for resultado in resultados for o in resultado.ofertas]
    marcadores = {o.barbearia.id: dict(lat=o.barbearia.latitude,
                                       lng=o.barbearia.longitude,
                                       titulo=o.barbearia.nome,
                                       detalhe=o.barbearia.endereco)
                  for o in ofertas}
    return render_template("barbeiro/busca.html", bairro=bairro,
                           resultados=resultados,
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


@bp.post("/agendamentos/<agendamento_id>/cancelar")
@requer_papel("barbeiro")
def cancelar_agendamento(agendamento_id):
    try:
        container().cancelar_agendamento.executar(
            barbeiro_id=usuario_id(), agendamento_id=agendamento_id)
    except (AcessoNegado, DadosInvalidos, NaoEncontrado) as erro:
        flash(str(erro), "erro")
    return redirect(url_for("barbeiro.painel"))


@bp.get("/barbearias/<barbearia_id>")
@requer_papel("barbeiro")
def perfil_da_barbearia(barbearia_id):
    barbearia = container().consultar_perfil_da_barbearia.executar(
        barbearia_id)
    return render_template("barbearia/perfil.html", barbearia=barbearia)
