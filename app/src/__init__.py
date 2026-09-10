from flask import Blueprint

marcas_bp = Blueprint('marca',__name__,url_prefix='/api/marca')
inventario_bp = Blueprint('inventario',__name__,url_prefix='/api/inventario')
cliente_bp = Blueprint('cliente', __name__,url_prefix='/api/cliente')
pagamentos_bp = Blueprint('pagemento', __name__, url_prefix='/api/pagamentos')