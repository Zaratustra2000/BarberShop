"""Controllers do dono (US2): traduzem formulários em chamadas de casos de
uso e o resultado em HTML. Nenhuma regra de negócio mora aqui."""
from flask import (Blueprint, flash, redirect, render_template, request,
                   url_for)

from app.formatos import (ler_data_hora, ler_decimal, ler_inteiro,
                          reais_para_centavos)
from app.routes.sessao import container, requer_papel, usuario_id
from domain.erros import DadosInvalidos
from use_cases.validar_foto_da_barbearia import LIMITE_DE_FOTO

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


@bp.post("/barbearias/<barbearia_id>/perfil")
@requer_papel("dono")
def editar_perfil(barbearia_id):
    form = request.form
    barbearia = container().editar_perfil_da_barbearia.executar(
        dono_id=usuario_id(), barbearia_id=barbearia_id,
        nome=form.get("nome", ""), endereco=form.get("endereco", ""),
        bairro=form.get("bairro", ""),
        latitude=ler_decimal(form.get("latitude"), "latitude"),
        longitude=ler_decimal(form.get("longitude"), "longitude"),
        regras=form.get("regras", ""),
        quantidade_de_cadeiras=ler_inteiro(
            form.get("quantidade_de_cadeiras"), "quantidade de cadeiras"))
    return redirect(url_for("dono.barbearia", barbearia_id=barbearia.id))


@bp.post("/barbearias/<barbearia_id>/foto")
@requer_papel("dono")
def atualizar_foto(barbearia_id):
    arquivo = request.files.get("foto")
    if arquivo is None or not arquivo.filename:
        flash("Envie uma imagem JPG, PNG ou WebP.", "erro")
        return redirect(url_for("dono.barbearia",
                                barbearia_id=barbearia_id))

    conteudo = arquivo.read(LIMITE_DE_FOTO + 1)
    try:
        extensao = container().validar_foto_da_barbearia.executar(conteudo)
    except DadosInvalidos as erro:
        flash(str(erro), "erro")
        return redirect(url_for("dono.barbearia",
                                barbearia_id=barbearia_id))

    anterior = container().consultar_barbearias_do_dono.uma(
        usuario_id(), barbearia_id)
    nome_gerado = container().fotos.salvar(conteudo, extensao)

    container().editar_perfil_da_barbearia.atualizar_foto_principal(
        dono_id=usuario_id(), barbearia_id=barbearia_id,
        nome_do_arquivo=nome_gerado)

    if anterior.foto_principal:
        container().fotos.remover(anterior.foto_principal)

    return redirect(url_for("dono.barbearia", barbearia_id=barbearia_id))


@bp.post("/barbearias/<barbearia_id>/cadeiras/<cadeira_id>/remover")
@requer_papel("dono")
def remover_cadeira(barbearia_id, cadeira_id):
    container().editar_perfil_da_barbearia.remover_cadeira(
        dono_id=usuario_id(), barbearia_id=barbearia_id,
        cadeira_id=cadeira_id)
    return redirect(url_for("dono.barbearia", barbearia_id=barbearia_id))
