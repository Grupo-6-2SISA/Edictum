import os
import time
import threading
from dotenv import load_dotenv
from twilio.rest import Client

# Carregar variáveis do .env
load_dotenv()

def _monitorar_status(client, sid, destinatario):
    """Monitora o status do SMS em segundo plano e loga quando houver atualização."""
    status_anterior = None
    while True:
        try:
            msg = client.messages(sid).fetch()
            status_atual = msg.status

            # Só loga quando houver mudança de status
            if status_atual != status_anterior:
                print(f"[TRACK] {destinatario} | SID: {sid} | Status: {status_atual}")
                status_anterior = status_atual

            # Se o status for final, encerra a thread
            if status_atual in ["delivered", "failed", "undelivered"]:
                print(f"[FINAL] {destinatario} | SID: {sid} | Status final: {status_atual}")
                break

            time.sleep(5)  # espera 5s antes de verificar novamente

        except Exception as e:
            print(f"[ERRO TRACK] Falha ao monitorar status do SMS {sid}: {str(e)}")
            break


def enviar_sms(mensagem: str, destinatario: str):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')

    try:
        client = Client(account_sid, auth_token)

        # Envia o SMS
        message = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=mensagem,
            to=destinatario
        )

        print(f"[SMS] Mensagem enviada para {destinatario}")
        print(f"      Message SID: {message.sid}")
        print(f"      Status inicial: {message.status}")

        # Inicia thread de monitoramento
        threading.Thread(
            target=_monitorar_status,
            args=(client, message.sid, destinatario),
            daemon=True
        ).start()

        return message.sid

    except Exception as e:
        print(f"[ERRO SMS] Falha ao enviar SMS para {destinatario}: {str(e)}")
        return None
