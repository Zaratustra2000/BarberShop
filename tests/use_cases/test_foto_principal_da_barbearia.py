from use_cases.editar_perfil_da_barbearia import EditarPerfilDaBarbearia
from use_cases.cadastrar_barbearia import CadastrarBarbearia


def test_dono_atualiza_foto_principal(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = CadastrarBarbearia(ctx.usuarios, ctx.barbearias).executar(
        dono_id=dono.id, nome="Barbearia Exemplo",
        endereco="Rua Exemplo, 100", bairro="Botafogo",
        latitude=-22.951, longitude=-43.184,
        regras="", quantidade_de_cadeiras=1)
    EditarPerfilDaBarbearia(
        ctx.usuarios, ctx.barbearias).atualizar_foto_principal(
            dono_id=dono.id, barbearia_id=barbearia.id,
            nome_do_arquivo="barbearia-1.webp")
    salva = ctx.barbearias.por_id(barbearia.id)
    assert salva.foto_principal == "barbearia-1.webp"
