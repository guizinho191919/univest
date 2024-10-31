import pandas as pd
from app.models import Venda, VendaProduto
from app import db
from prophet import Prophet

def prever_demanda(produto_id, periodo=30):
    vendas = db.session.query(
        Venda.dataVenda.label('ds'),
        VendaProduto.quantidadeProduto.label('y')
    ).join(VendaProduto, Venda.id == VendaProduto.vendaId
    ).filter(VendaProduto.produtoId == produto_id
    ).order_by(Venda.dataVenda).all()
    
    if not vendas or len(vendas) < 2:
        return None
    
    dados = pd.DataFrame(vendas)
    
    modelo = Prophet()
    modelo.fit(dados)
    
    futuro = modelo.make_future_dataframe(periods=periodo)
    forecast = modelo.predict(futuro)
    
    previsoes = forecast[['ds', 'yhat']].tail(periodo)
    return previsoes
