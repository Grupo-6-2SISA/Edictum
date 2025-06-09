# core/services/email_service.py

"""

falta implementar logs de envio de email, que depende da inclusão da fk_cliente nesta tabela. (kotlin)

"""

import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import mimetypes
import os
from typing import Union

# Carregar variáveis do .env
load_dotenv()

def enviar_email(destinatario: Union[str, list[str]], assunto: str, corpo: str, cc: list[str] = None, bcc: list[str] = None):
    remetente = os.getenv('EMAIL_SENDER')
    senha = os.getenv('EMAIL_PASSWORD')

    # Normaliza para lista, mesmo que seja apenas uma string
    destinatario = [destinatario] if isinstance(destinatario, str) else destinatario

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = ', '.join(destinatario)

    if cc:
        msg['Cc'] = ', '.join(cc)

    # Cópia oculta (Bcc) não vai no header, só no envelope
    destinatarios_totais = destinatario + (cc or []) + (bcc or [])

    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg, to_addrs=destinatarios_totais)
        print(f"[EMAIL] Mensagem enviada para {destinatario}")
    except Exception as e:
        print(f"[ERRO EMAIL] Falha ao enviar para {destinatario}: {str(e)}")


def enviar_email_com_ics(destinatario: str, assunto: str, corpo: str, caminho_ics: str):
    remetente = os.getenv('EMAIL_SENDER')
    senha = os.getenv('EMAIL_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content(corpo)

    # Ler e anexar o arquivo .ics
    try:
        with open(caminho_ics, 'rb') as f:
            ics_data = f.read()

        tipo_mime, _ = mimetypes.guess_type(caminho_ics)
        if tipo_mime is None:
            tipo_mime = 'application/octet-stream'
        maintype, subtype = tipo_mime.split('/')

        msg.add_attachment(ics_data, maintype=maintype, subtype=subtype, filename=os.path.basename(caminho_ics))
    except Exception as e:
        print(f"[ERRO] Falha ao anexar o arquivo .ics: {str(e)}")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
        print(f"[EMAIL] Mensagem enviada para {destinatario} com anexo .ics")
    except Exception as e:
        print(f"[ERRO EMAIL] Falha ao enviar para {destinatario}: {str(e)}")
