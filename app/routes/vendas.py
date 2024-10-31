from flask import Blueprint, request, jsonify
from app.models import Produto, Venda, VendaProduto
from app import db
from sqlalchemy import func
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/relatorio_vendas', methods=['GET'])
def relatorio_vendas():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio or not data_fim:
        return jsonify({'erro': 'Parâmetros data_inicio e data_fim são necessários.'}), 400
    
    # Converter as datas de string para objetos datetime
    try:
        data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
    
    resultados = db.session.query(
        Produto.nome.label('nome_produto'),
        func.sum(VendaProduto.quantidadeProduto).label('quantidade_vendida'),
        func.sum(VendaProduto.precoVenda * VendaProduto.quantidadeProduto).label('total_vendas')
    ).join(VendaProduto, Produto.id == VendaProduto.produtoId
    ).join(Venda, Venda.id == VendaProduto.vendaId
    ).filter(Venda.dataVenda.between(data_inicio_dt, data_fim_dt)
    ).group_by(Produto.id
    ).order_by(db.desc('quantidade_vendida')).all()
    
    dados = []
    for resultado in resultados:
        dados.append({
            'nome_produto': resultado.nome_produto,
            'quantidade_vendida': int(resultado.quantidade_vendida),
            'total_vendas': float(resultado.total_vendas)
        })
    
    return jsonify(dados)
