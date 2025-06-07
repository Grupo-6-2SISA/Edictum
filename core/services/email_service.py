import smtplib
from email.message import EmailMessage

def enviar_email(destinatario: str, assunto: str, corpo: str):
    remetente = 'marciorjuliao22@gmail.com'
    senha = 'sua_senha_de_app'  # Use senha de app para Gmail

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
        print(f"[EMAIL] Mensagem enviada para {destinatario}")
    except Exception as e:
        print(f"[ERRO EMAIL] Falha ao enviar para {destinatario}: {str(e)}")
