from flask import Blueprint, jsonify
from app.models import Produto
from datetime import datetime, timedelta

validade_bp = Blueprint('validade', __name__)

@validade_bp.route('/alerta_validade', methods=['GET'])
def alerta_validade():
    hoje = datetime.now()
    data_alerta = hoje + timedelta(days=7)
    produtos = Produto.query.filter(Produto.dataValidade <= data_alerta).all()
    
    dados = []
    for produto in produtos:
        dias_restantes = (produto.dataValidade - hoje).days
        dados.append({
            'id': produto.id,
            'nome': produto.nome,
            'dataValidade': produto.dataValidade.strftime('%Y-%m-%d'),
            'dias_restantes': dias_restantes
        })
    
    return jsonify(dados)
