from flask import Blueprint, request, jsonify
from app.utils.previsao_demanda import prever_demanda

previsao_bp = Blueprint('previsao', __name__)

@previsao_bp.route('/previsao_demanda', methods=['GET'])
def previsao_demanda():
    produto_id = request.args.get('produto_id')
    periodo = request.args.get('periodo', default=30, type=int)
    
    if not produto_id:
        return jsonify({'erro': 'Parâmetro produto_id é necessário.'}), 400
    
    previsoes = prever_demanda(produto_id, periodo)
    if previsoes is None:
        return jsonify({'erro': 'Dados insuficientes para previsão.'}), 400
    
    dados = previsoes.to_dict(orient='records')
    return jsonify(dados)
