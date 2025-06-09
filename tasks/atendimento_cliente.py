from core.services import email_service as es

def run():
    es.enviar_email('marciorjuliao@gmail.com', 'assunto', 'corpo')
