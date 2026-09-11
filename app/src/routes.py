from flask import request, jsonify
from flask_login import login_required,current_user

from app.src import marcas_bp
from app.src import inventario_bp
from app.src import cliente_bp
from app.src import pagamentos_bp # Organização Blueprint

from app.extensions import db

from app.models import Marcas,Inventario,Clientes,Pagamentos

@marcas_bp.route ('/add', methods = ["POST"])
@login_required
def add_marcas():
    data = request.json
    if 'nome_marcas' in data and 'origem' in data:
        marcas = Marcas(nome_marcas=data["nome_marcas"], origem=data["origem"])
        db.session.add(marcas)
        db.session.commit()
        return jsonify ({"mensagem":"Marca Adicionado com Sucesso"}), 201
    return jsonify ({"mensagem":"Dados da Marca do Veiculo Invalida"}), 400

@marcas_bp.route('/delete/<int:marcas_id>', methods =["DELETE"])
@login_required
def delete_marca(marcas_id):
    marcas = Marcas.query.get(marcas_id)
    if marcas:
        db.session.delete(marcas)   
        db.session.commit()
        return jsonify ({"mensagem":"Marca Deletada com Sucesso"}), 200
    return jsonify ({"mensagem":"Marca do Veiculo não Encontrada"}), 400
 
@marcas_bp.route('/<int:marcas_id>', methods = ["GET"])
@login_required 
def get_marca(marcas_id):
    marcas = Marcas.query.get(marcas_id)
    if marcas:
        return jsonify({
            'id':marcas.id,
            'nome_marcas':marcas.nome_marcas,
            'origem':marcas.origem
        })
    return jsonify ({"mensagem":"Marca do Veiculo naõ Encontrada"}), 404

@marcas_bp.route('/upadate/<int:marcas_id>', methods = ["PUT"])
@login_required
def edit_marca(marcas_id):
    marcas = Marcas.query.get(marcas_id)
    if not marcas:
        return jsonify ({"mensagem":"Veiculo não Encontrado"}), 404
    data = request.json
    if 'nome_marcas' in data:
        marcas.nome_marcas = data['nome_marcas']
        
    if 'origem' in data:
        marcas.origem = data['origem']    
    
    db.session.commit()
    return jsonify ({"mensagem":"Veiculo Atualizado com Sucesso"}), 200

@marcas_bp.route('/', methods = ['GET'])
@login_required
def get():
    marcas = Marcas.query.all()
    marcas_list = []
    for marca in marcas:
        marcas_data = {
            'id':marca.id,
            'nome_marcas':marca.nome_marcas,
            'origem':marca.origem
        }
        marcas_list.append(marcas_data)
    return jsonify (marcas_list)