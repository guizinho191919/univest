from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações da aplicação
app.config['SECRET_KEY'] = 'sua_chave_secreta'  # Substitua por uma chave segura

# Definir o caminho completo para o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/guilherme.alencar/supermercado_garibaldi/database.db'

# Opcional: imprimir o caminho do banco de dados para verificação
print('Database URI:', app.config['SQLALCHEMY_DATABASE_URI'])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização da extensão SQLAlchemy
db = SQLAlchemy(app)

# Importar os modelos
from app import models

# Importar e registrar os blueprints das rotas
from app.routes.vendas import vendas_bp
from app.routes.validade import validade_bp
from app.routes.previsao import previsao_bp

app.register_blueprint(vendas_bp)
app.register_blueprint(validade_bp)
app.register_blueprint(previsao_bp)
