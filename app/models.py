from flask_login import UserMixin
from app.extensions import db

class Marcas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_marcas = db.Column(db.String(255), nullable=False)
    origem = db.Column(db.String(255), nullable=False)
    
class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(255), nullable=False)
    transmissao = db.Column(db.String(255), nullable=False)
    motor = db.Column(db.String(255), nullable=False)
    combustivel = db.Column(db.String(255), nullable=False)
    marcas = db.relationship('Marcas', backref='Inventario', lazy = True)
    marcas_id = db.Column(db.Integer, db.ForeignKey('marcas.id'))

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(255), nullable=False)
    sobrenome_cliente = db.Column(db.String(255), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    
class Pagamentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor_pago = db.Column(db.Numeric(10,2), nullable=False)
    data_pagamentos = db.Column(db.Date,nullable=False)
    inventario = db.relationship('Inventario', backref='Pagamentos', lazy = True)
    clientes = db.relationship('Clientes', backref='Pagamentos', lazy =True)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))
    clientes_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    
    