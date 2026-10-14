from datetime import datetime
from decimal import Decimal 

from sqlalchemy import func

from app.extensions import db
from app.models import Locacoes, Pagamentos
from app.service.locacoes_service import RegraNegocioError

Centavos = Decimal('0.01')

def total_pago(locacao_id, ignorar_pagamento_id=None):
    consulta = db.session.query(func.coalesce(func.sum(Pagamentos.valor_pago), 0)).filter(
        Pagamentos.locacao_id == locacao_id
    )
    if ignorar_pagamento_id is not None:
        consulta = consulta.filter(Pagamentos.id != ignorar_pagamento_id)
    return Decimal (str(consulta.scalar())).quantize(Centavos)

def resumo_pagamento(locacao):
    pago = total_pago(locacao.id)
    return pago, locacao.valor - pago

def converter_valor(valor):
    if not isinstance(valor,(int,float)) or isinstance (valor, bool) or valor <= 0:
        raise RegraNegocioError ("valor de pagamento invalido")
    return Decimal(str(valor)).quantize(Centavos)

def converter_data(texto):
    try:
        return datetime.strptime(texto,'%Y-%m-%d').date()
    except(ValueError, TypeError):
        raise RegraNegocioError ("Formato de Data invalido")

def validar_saldo(locacao,valor,ignorar_pagamento_id=None):
    if total_pago (locacao.id, ignorar_pagamento_id) + valor > locacao.valor:
        raise RegraNegocioError ("Pagamento execede o saldo da locação", status_code=409)

def criar_pagamento(data):
    locacao = Locacoes.query.get(data.get('locacao_id'))
    if not locacao:
        raise RegraNegocioError ("Locação não encontrada", status_code=404)
    if locacao.status_locacao == 'CANCELADA':
        raise RegraNegocioError ("Locação cancelada não aceita pagamento", status_code=409)

    valor = converter_valor(data.get('valor_pago'))
    data_pagamento = converter_data(data.get('data_pagamentos'))
    validar_saldo(locacao, valor)

    pagamento = Pagamentos(
        valor_pago=valor,
        data_pagamentos=data_pagamento,
        locacao_id=locacao.id
    )
    db.session.add(pagamento)
    db.session.commit()
    return pagamento


def atualizar_pagamento(pagamento_id, data):
    pagamento = Pagamentos.query.get(pagamento_id)
    if not pagamento:
        raise RegraNegocioError ("Pagamento não Encontrado", status_code=404)
    if 'valor_pago' in data:
        valor = converter_valor(data['valor_pago'])
        validar_saldo(pagamento.locacao, valor, ignorar_pagamento_id=pagamento_id)
        pagamento.valor_pago = valor
    if 'data_pagamentos' in data:
        pagamento.data_pagamentos = converter_data(data['data_pagamentos'])

    db.session.commit()
    return pagamento