from app import db
from sqlalchemy import TypeDecorator, BigInteger
from datetime import datetime

class MillisecondTimestamp(TypeDecorator):
    impl = BigInteger

    def process_bind_param(self, value, dialect):
        if value is not None:
            return int(value.timestamp() * 1000)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return datetime.fromtimestamp(value / 1000)
        return None

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoqueAtual = db.Column(db.Integer, nullable=False)
    dataValidade = db.Column(MillisecondTimestamp, nullable=False)
    dataCadastro = db.Column(MillisecondTimestamp, nullable=False)
    categoriaId = db.Column(db.String, db.ForeignKey('categoria.id'), nullable=False)
    
    vendaProdutos = db.relationship('VendaProduto', backref='produto', lazy=True)

class Venda(db.Model):
    __tablename__ = 'venda'
    id = db.Column(db.String, primary_key=True)
    dataVenda = db.Column(MillisecondTimestamp, nullable=False)
    
    vendaProdutos = db.relationship('VendaProduto', backref='venda', lazy=True)

class VendaProduto(db.Model):
    __tablename__ = 'vendaProduto'
    id = db.Column(db.String, primary_key=True)
    quantidadeProduto = db.Column(db.Integer, nullable=False)
    precoVenda = db.Column(db.Float, nullable=False)
    produtoId = db.Column(db.String, db.ForeignKey('produto.id'), nullable=False)
    vendaId = db.Column(db.String, db.ForeignKey('venda.id'), nullable=False)
