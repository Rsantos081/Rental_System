from app.extensions import db
from decimal import Decimal, ROUND_HALF_UP
from app.models import Clientes, Inventario, Locacoes
from datetime import datetime

STATUS_LOCACAO_VALIDOS = {'ATIVA', 'ATRASADA', 'FINALIZADA', 'CANCELADA'}

STATUS_QUE_BLOQUEIAM_VEICULO = ['ATIVA','ATRASADA']

TRANSICOES_PERMITIDAS = {
    'ATIVA': {'FINALIZADA', 'ATRASADA', 'CANCELADA'},
    'ATRASADA': {'FINALIZADA'},
    'FINALIZADA': set(),
    'CANCELADA': set(),
}

class RegraNegocioError(Exception):
    def __init__(self,mensagem,status_code=400):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code
        
def calcular_valor(data_incio, data_prevista_devolucao, valor_diaria):
    dias = (data_prevista_devolucao - data_incio).days
    return (Decimal(dias) * Decimal(valor_diaria)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def criar_locacao(data):

    cliente = Clientes.query.get(data.get('clientes_id'))
    if not cliente:
        raise RegraNegocioError("Cliente não encontrado")

    inventario = Inventario.query.get(data.get('inventario_id'))
    if not inventario:
        raise RegraNegocioError("Veiculo não Encontrado")
    
    if inventario.valor_diaria is None or inventario.valor_diaria <= 0:
        raise RegraNegocioError("Veiculo sem valor de diaria cadastrado")
    
    locacao_aberta = Locacoes.query.filter(
        Locacoes.inventario_id == data['inventario_id'],
        Locacoes.status_locacao.in_(STATUS_QUE_BLOQUEIAM_VEICULO)
    ). first()
    if locacao_aberta:
        raise RegraNegocioError("Veiculo ja esta alugado", status_code= 409)
    try: 
      data_inicio = datetime.strptime(data.get('data_inicio'), '%Y-%m-%d').date()
      data_prevista_devolucao = datetime.strptime(data.get('data_prevista_devolucao'),'%Y-%m-%d').date()
    except (ValueError,TypeError):
        raise RegraNegocioError ("Formato de Data Invalido")
    
    if data_prevista_devolucao <= data_inicio:
        raise RegraNegocioError ("Data de Devolução deve ser posterior a data de inicioent")
    valor = calcular_valor(data_inicio,data_prevista_devolucao, inventario.valor_diaria)    
    
    locacao = Locacoes(
        data_inicio=data_inicio,
        data_prevista_devolucao=data_prevista_devolucao,
        status_locacao='ATIVA',
        valor=valor,
        inventario_id=data['inventario_id'],
        clientes_id=data['clientes_id']
    )
    db.session.add(locacao)
    db.session.commit()
    return locacao


def atualizar_status_locacao(locacoes_id, novo_status):
    locacao = Locacoes.query.get(locacoes_id)
    if not locacao:
        raise RegraNegocioError("Locação não Encontrada")

    if novo_status not in STATUS_LOCACAO_VALIDOS:
        raise RegraNegocioError("Status invalido")

    if novo_status not in TRANSICOES_PERMITIDAS.get(locacao.status_locacao, set()):
        raise RegraNegocioError("Transição de status não permitida", status_code = 409)
    
    locacao.status_locacao = novo_status
    db.session.commit()
    return locacao