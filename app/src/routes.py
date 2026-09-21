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

@inventario_bp.route('/add', methods = ["POST"])
@login_required
def add_modelo():
    data = request.json
    if 'modelo' in data and 'transmisao' in data and 'motor' in data and 'combustivel' in data and 'marcas_id' in data:
        marca = Marcas.query.get(data['marcas_id'])
        if not marca:
            return jsonify ({"mensagem":"Marca não Encontrada"}), 404
        inventarios = Inventario(
                modelo=data['modelo'], 
                transmisao=data['transmisao'], 
                motor=data['motor'], 
                combustivel=data['combustivel'],
                marcas_id =data['marcas_id']
        )   
        db.session.add(inventarios)
        db.session.commit()
        return jsonify ({"mensagem":"Modelo de Carro Adicionado com Sucesso"}), 201
    return jsonify ({"mensagem":"Crendencias do Modelo Invalido"}), 400

@inventario_bp.route('/delete/<int:inventario_id>', methods = ['DELETE'])
@login_required
def delete_modelo(inventario_id):
    inventarios = Inventario.query.get(inventario_id)
    if inventarios:
        db.session.delete(inventarios)
        db.session.commit()
        return jsonify ({"mensagem":"Modelo de carro deletado com sucesso"}), 200
    return jsonify ({"mensagem":"Modelo de carro nao Encontrado"}), 400

@inventario_bp.route('/<int:inventario_id>', methods = ["GET"])
@login_required
def get_modelo(inventario_id):
    inventarios = Inventario.query.get(inventario_id)
    if inventarios:
        return jsonify ({
            'id': inventarios.id,
            'modelo':inventarios.modelo,
            'transmisao':inventarios.transmisao,
            'motor':inventarios.motor,
            'combustivel':inventarios.combustivel,
            'marcas_id':inventarios.marcas_id
        })
    return jsonify ({"mensagem":"Modelo de carro nao encontrado"}), 404

@inventario_bp.route('/<int:inventario_id>', methods = ["PUT"])
@login_required
def mod_modelo(inventario_id):
    inventarios = Inventario.query.get(inventario_id)
    if not inventarios:
        return jsonify ({"mensagem":"Produto não Encontrado"}), 404
    data = request.json
    if 'modelo' in data:
        inventarios.modelo = data['modelo']
        
    if 'transmissao' in data:
        inventarios.transmissao = data['transmissao']
    
    if 'motor' in data:
        inventarios.motor = data['motor']
    
    if 'combustivel' in data:
        inventarios.combustivel = data['combustivel']

    db.session.commit()
    return jsonify ({"mensagem":"Produto Atualizado com Sucesso"}), 200         

@inventario_bp.route('/', methods = ['GET'])
@login_required
def get():
    inventario = Inventario.query.all()
    inventario_list = []
    for inventarios in inventario:
        inventario_date ={
            'id':inventarios.id,
            'modelo':inventarios.modelo,
            'transmissao':inventarios.transmissao,
            'motor':inventarios.motor,
            'combustivel':inventarios.combustivel,
            'marcas_id':inventarios.marcas_id
        }
        inventario_list.append(inventario_date)
    return jsonify (inventario_list)

@cliente_bp.route('/add', methods = ['POST'])
@login_required
def add_cliente():
    data = request.json
    if 'nome_cliente' in data and 'sobrenome_cliente' in data and 'endereco' in data and 'cpf' in data:
       cliente = Clientes.query.filter_by(cpf = data['cpf']).first()
       if  cliente:
           return jsonify ({"mensagme":"Cliente ja Existe"})
       clientes = Clientes(
           nome_cliente = data['nome_cliente'],
           sobrenome_cliente = data['sobrenome_cliente'],
           cpf = data['cpf'],
           endereco = data['endereco']           
       )
       db.session.add(clientes)
       db.session.commit()
       return jsonify ({"mensagem":"Cliente Adicionado com Sucesso"}), 200
    return jsonify ({"mensagme":"Dados Inserido Invalidos"}),400

@cliente_bp.route('/delete/<int:cliente_id>', methods = ['DELETE'])
@login_required
def delete_cliente(cliente_id):
    cliente = Clientes.query.get(cliente_id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify ({"mensagem":"Cliente Apagado com Sucesso"}), 200
    return jsonify ({"mensagem":"Cliente não encontrado, Dados invalidos"}), 404

@cliente_bp.route('/<int:cliente_id>', methods = ['GET'])
@login_required
def get_cliente(cliente_id):
    cliente = Clientes.query.get(cliente_id)
    if cliente:
        return jsonify({
            'nome_cliente': cliente.nome_cliente,
            'sobrenome_cliente': cliente.sobrenome_cliente,
            'endereco': cliente.endereco,
            'cpf': cliente.cpf            
        })
    return jsonify ({"mensagem":"Cliente não Encontrado"}), 400

@cliente_bp.route('/update/<int:clientes_id>', methods = ['PUT'])
@login_required
def update_cliente(clientes_id):
    cliente = Clientes.query.get(clientes_id)
    if not cliente:
        return jsonify ({"mensagem":"Cliente não Encontrado"}), 404
    data = request.json
    if 'nome_cliente' in data:
        cliente.nome_cliente = data['nome_cliente']
        
    if 'sobrenome_cliente' in data:
        cliente.sobrenome_cliente = data['sobrenome_cliente']
        
    if 'endereco' in data:
        cliente.endereco = data['endereco']
        
    if 'cpf' in data:
        cliente.cpf = data['cpf']
    db.session.commit()
    return jsonify ({"mensagem":"Dados do Cliente Atualizado com Sucesso"}), 200

@cliente_bp.route('/', methods = ['GET'])
@login_required
def cliente():
    cliente = Clientes.query.all()
    cliente_list = []
    for clientes in cliente:
        clientes_date= {
            'id':clientes.id,
            'nome_cliente':clientes.nome_cliente,
            'sobrenome_cliente':clientes.sobrenome_cliente,
            'endereco':clientes.endereco,
            'cpf':clientes.cpf
        }
        cliente_list.append(clientes_date)
    return jsonify (cliente_list)
    
@pagamentos_bp.route('/add', methods = ['POST'])
@login_required
def add_pagamento():
    