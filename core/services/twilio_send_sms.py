import os

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

def enviar_sms(mensagem: str, destinatario: str):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid=os.getenv('TWILIO_MESSAGING_SERVICE_SID'),
        body=mensagem,
        to=destinatario
        # Exemplo de destinatario: "+5511999999999" (com código do país - sempre brasil)
    )
    print(message.sid)