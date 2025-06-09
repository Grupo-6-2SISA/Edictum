import os
from core import database as db
from core.services import email_service as es
def run():
    aniversariantes = db.executarSelect("SELECT * FROM cliente WHERE DATE_FORMAT(data_nascimento, '%m-%d') = DATE_FORMAT(CURDATE(), '%m-%d') AND cnpj IS NULL")

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
            try:
                es.enviar_email(destinatario=email, assunto="Feliz Aniversário!", corpo=mensagem, bcc=[os.getenv('EMAIL_MONITOR')])
                db.executarQuery("INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                                 f"(null, {cliente['id_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar email de aniversário para {nome} ({email})')")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar email para {nome} ({email}): {str(e)}")
                db.executarQuery("INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                                 f"(null, {cliente['id_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar email de aniversário para {nome} ({email}): {str(e)}')")
                continue

        return "Aniversários enviados com sucesso!"
    else:
        print("[INFO] Nenhum aniversariante encontrado para hoje.")
        return "Nenhum aniversariante encontrado para hoje."