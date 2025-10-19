import os
from core import database as db
from core.services import email_service as es
from core.services import twilio_send_sms as sms
def run():
    aniversariantes = db.executarSelect("SELECT * FROM cliente WHERE DATE_FORMAT(data_nascimento, '%m-%d') = DATE_FORMAT(CURDATE(), '%m-%d') AND cnpj IS NULL")

    if aniversariantes:
        for cliente in aniversariantes:
            nome = cliente['nome']
            email = cliente['email']
            telefone = cliente['telefone']
            mensagem_email = f"""
            Prezado(a) {nome},
            
            Em nome de toda a equipe do escritório Orlando Matos Advogados Associados, queremos lhe desejar um feliz aniversário!
            
            Que este novo ciclo traga ainda mais conquistas, saúde, alegria e realizações. Conte sempre conosco para o que precisar — é um privilégio tê-lo(a) como cliente.
            
            Com os melhores votos,
            
            Orlando Matos Advogados Associados
            """
            mensagem_sms = f"Feliz aniversário, {nome}! 🎉 Que seu dia seja especial. Abraços da equipe Orlando Matos Advogados Associados."

            try:
                es.enviar_email(destinatario=email, assunto="Feliz Aniversário! | Orlando Matos Advogados Associados", corpo=mensagem_email, bcc=[os.getenv('EMAIL_MONITOR')])
                db.executarQuery("INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                                 f"(1, null, {cliente['id_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar email de aniversário para {nome} ({email})')")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar email para {nome} ({email}): {str(e)}")
                erro_sql = str(e).replace("'", "''")
                db.executarQuery("INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                                 f"(1, null, {cliente['id_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar email de aniversário para {nome} ({email}): {str(erro_sql)}')")
            try:
                sms.enviar_sms(mensagem=mensagem_sms ,destinatario=telefone)
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(1, null, {cliente['id_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar sms de aniversário para {nome} ({telefone})')")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar SMS para {nome} ({telefone}): {str(e)}")
                erro_sql = str(e).replace("'", "''")
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(1, null, {cliente['id_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar sms de aniversário para {nome} ({telefone}): {str(erro_sql)}')")
            continue

        return f"Aniversários enviados com sucesso! Quantidade: {len(aniversariantes)}"
    else:
        print("[INFO] Nenhum aniversariante encontrado para hoje.")
        return "Nenhum aniversariante encontrado para hoje."