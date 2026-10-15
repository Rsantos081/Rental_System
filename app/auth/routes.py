from flask import jsonify, request
from flask_login import  logout_user,login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.auth import auth_bp
from app.extensions import db, login_manager
from app.models import Administrador

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Administrador, int(user_id))

@auth_bp.route('/login', methods =['POST'])
def login():
    data = request.get_json(silent=True) or {}
    user = Administrador.query.filter_by(nome=data.get("nome")).first()
    
    if user and check_password_hash(user.senha, data.get("senha") or ""): # O check_password_hash ele tem objetivo de verificar se a senha inserida esta correta ou incorreta, caso de correta ele tera acesso a sua conta
        login_user(user)
        return jsonify ({"mensagme":"Administrador logado com sucesso"}), 200
    return jsonify ({"mensagem":"Credenciais invalidas"}), 401

@auth_bp.route('/logout', methods = ['POST'])
@login_required
def lougout():
    logout_user()
    return jsonify ({"mensagem":"Logout realizado com sucesso"}), 200

@auth_bp.route('/registro', methods = ['POST'])
@login_required
def registro():
    data = request.get_json(silent=True) or {}
    nome = data.get("nome")
    sobrenome = data.get("sobrenome")
    cpf = data.get('cpf')
    senha = data.get('senha')
    
    if not nome or not sobrenome or not cpf or not senha:
        return jsonify ({"mensagem":"Dados invalidos, observe os campos"}), 400
    if Administrador.query.filter_by((nome == nome) | (Administrador.cpf == cpf)).first():
        return jsonify ({"mensagem":"Administrador ja existe"}), 402
    
    admin = Administrador(nome=nome , sobrenome=sobrenome , cpf = cpf, senha=generate_password_hash(senha)) # Campo responsavel por não cadastrar uma senha padrao no banco como (minha_senha123), ele cadastrar uma pedaço de texto de string aleatorias.
    db.session.add(admin)
    db.session.commit()
    return jsonify ({"mensagem":"Administrador registrado com sucesso"}), 201
