import os
from core import database as db
from core.services import email_service as es
def run():
    aniversariantes = db.executarSelect("SELECT * FROM cliente WHERE DATE_FORMAT(data_nascimento, '%m-%d') = DATE_FORMAT(CURDATE(), '%m-%d');")

    aniversariantes = [x for x in aniversariantes if x['cnpj'] is None]

    if aniversariantes:
        for cliente in aniversariantes:
            nome = cliente['nome']
            email = cliente['email']
            mensagem = mensagem = f"""
            Prezado(a) {nome},
            
            Em nome de toda a equipe do escritório Orlando Matos Advogados Associados, queremos lhe desejar um feliz aniversário!
            
            Que este novo ciclo traga ainda mais conquistas, saúde, alegria e realizações. Conte sempre conosco para o que precisar — é um privilégio tê-lo(a) como cliente.
            
            Com os melhores votos,
            
            Orlando Matos Advogados Associados
            """

            es.enviar_email(destinatario=email, assunto="Feliz Aniversário!", corpo=mensagem, bcc=[os.getenv('EMAIL_MONITOR')])


    else:
        print("[INFO] Nenhum aniversariante encontrado para hoje.")
        return