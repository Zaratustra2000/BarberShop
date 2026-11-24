"""Controllers do cliente (US5)."""
from flask import Blueprint, redirect, render_template, request, url_for

from app.formatos import ler_data_hora
from app.routes.sessao import container, requer_papel, usuario_id

bp = Blueprint("cliente", __name__, url_prefix="/cliente")


@bp.get("")
@requer_papel("cliente")
def painel():
    c = container()
    nome = request.args.get("nome", "").strip()
    barbeiros = c.buscar_barbeiros.executar(nome)
    resultados = []
    for barbeiro in barbeiros:
        perfil = c.consultar_perfil_do_barbeiro.executar(barbeiro.id)
        tem_horario = False
        for servico in perfil.servicos:
            perfil_com_servico = c.consultar_perfil_do_barbeiro.executar(
                barbeiro.id, servico.id)
            if perfil_com_servico.horarios:
                tem_horario = True
                break
        resultados.append({
            "barbeiro": barbeiro,
            "tem_servico": bool(perfil.servicos),
            "tem_horario": tem_horario,
        })
    return render_template(
        "cliente/painel.html", nome=nome,
        barbeiros=resultados,
        agendamentos=c.consultar_agendamentos_do_cliente.executar(
            usuario_id()))


@bp.get("/barbeiros/<barbeiro_id>")
@requer_papel("cliente")
def perfil_do_barbeiro(barbeiro_id):
    perfil = container().consultar_perfil_do_barbeiro.executar(
        barbeiro_id, request.args.get("servico_id"))
    locais = {i.barbearia.id: dict(lat=i.barbearia.latitude,
                                   lng=i.barbearia.longitude,
                                   titulo=i.barbearia.nome,
                                   detalhe=i.barbearia.endereco)
              for i in perfil.proximos_locais}
    return render_template("cliente/perfil_do_barbeiro.html", perfil=perfil,
                           marcadores=list(locais.values()))


@bp.post("/agendamentos")
@requer_papel("cliente")
def agendar():
    container().agendar_atendimento.executar(
        cliente_id=usuario_id(),
        servico_id=request.form.get("servico_id", ""),
        inicio=ler_data_hora(request.form.get("inicio")))
    return redirect(url_for("cliente.painel"))


@bp.get("/barbearias/<barbearia_id>")
@requer_papel("cliente")
def perfil_da_barbearia(barbearia_id):
    barbearia = container().consultar_perfil_da_barbearia.executar(
        barbearia_id)
    return render_template("barbearia/perfil.html", barbearia=barbearia)
