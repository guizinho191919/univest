from app.models import Produto
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

def enviar_alertas():
    hoje = datetime.now().date()
    data_alerta = hoje + timedelta(days=7)
    produtos = Produto.query.filter(Produto.data_validade <= data_alerta).all()

    if produtos:
        mensagem = "Produtos próximos da validade:\n"
        for produto in produtos:
            mensagem += f"- {produto.nome} (Validade: {produto.data_validade.strftime('%Y-%m-%d')})\n"

        enviar_email('destinatario@example.com', 'Alerta de Validade', mensagem)

def enviar_email(destinatario, assunto, mensagem):
    remetente = 'seuemail@example.com'
    senha = 'suasenha'

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
