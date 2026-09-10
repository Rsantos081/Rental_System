from flask import request, jsonify
from flask_login import login_required,current_user

from app.src import marcas_bp
from app.src import inventario_bp
from app.src import cliente_bp
from app.src import pagamentos_bp

from app.extensions import db

from app.models import Marcas,Inventario,Clientes,Pagamentos

