from flask import jsonify, request
from flask_login import  logout_user,login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.auth import auth_bp
from app.extensions import db
from app.models import Administrador

@auth_bp.route('/login', methods =['POST'])
def login():
    data = request.get_json(silent=True) or {}
    user = Administrador.query.filter_by(nome=data.get("nome")).first()
    
    if user and check_password_hash(user.senha, data.get("senha") or ""):
        login_user(user)
        return jsonify ({"mensagme":"Administrador logado com sucesso"}), 200
    return jsonify ({"mensagem":"Credenciais invalidas"}), 401

@auth_bp.route('/logout', methods = ['POST'])
@login_required
def lougout():
    logout_user()
    return jsonify ({"mensagem":"Logout realizado com sucesso"}), 204

@auth_bp.route('/registro', methods = ['POST'])
def registro():
    data = request.get_json(silent=True) or {}
    nome = data.get("nome")
    senha = data.get("senha")
    
    if not nome or not senha:
        return jsonify ({"mensagem":"Dados invalidos, observe os campos"}), 400
    if Administrador.query.filter_by(nome=nome).first():
        return jsonify ({"mensagem":"Administrador ja existe"}), 402
    admin = Administrador(nome=nome , senha=generate_password_hash(senha))
    db.session.add(admin)
    db.session.commit()
    return jsonify ({"mensagem":"Administrador registrado com sucesso"}), 201
