import os
from core import database as db
from core.services import email_service as es
from datetime import datetime as dt, timedelta


def run():

    link_pesquisa = os.getenv("LINK_PESQUISA")
    atendimentos_concluídos = db.executarSelect("""
    SELECT A.fk_cliente as id_cliente, D.nome as nome_cliente, D.email as email_cliente, B.data_hora_alteracao, C.descricao 
	FROM ATENDIMENTO A 
	INNER JOIN HISTORICO_STATUS_AGENDAMENTO B
		ON A.ID_ATENDIMENTO = B.FK_ATENDIMENTO
    INNER JOIN STATUS_AGENDAMENTO C
		ON C.ID_STATUS_AGENDAMENTO = B.FK_STATUS_AGENDAMENTO
	INNER JOIN CLIENTE D
		ON D.ID_CLIENTE = A.FK_CLIENTE
    WHERE C.DESCRICAO = 'Concluído'
	AND DATE(B.DATA_HORA_ALTERACAO) = CURRENT_DATE() - INTERVAL 1 DAY
    AND A.SHOULD_ENVIAR_EMAIL = 1;
    """)

    if atendimentos_concluídos:
        for atendimento_concluido in atendimentos_concluídos:
            nome = atendimento_concluido['nome_cliente']
            email = atendimento_concluido['email_cliente']
            mensagem = f"""
            Prezado(a) {nome},

            Em nome de toda a equipe do escritório Orlando Matos Advogados Associados, gostaríamos de agradecer pela confiança em nossos serviços. 
            
            Para nós, é fundamental entender sua experiência e identificar como podemos melhorar ainda mais o nosso atendimento. 
            Por isso, convidamos você a responder nossa pesquisa de satisfação. Sua opinião é muito importante para que possamos continuar evoluindo e oferecendo um serviço de excelência.

            Acesse a pesquisa pelo link abaixo:
            {link_pesquisa}

            Agradecemos desde já pela sua colaboração e pelo tempo dedicado.

            Atenciosamente,

            Orlando Matos Advogados Associados
            """
            try:
                es.enviar_email(destinatario=email, assunto="Sua opinião é muito importante para nós | Orlando Matos Advogados Associados", corpo=mensagem,
                                bcc=[os.getenv('EMAIL_MONITOR')])
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(5, null, {atendimento_concluido['id_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar email de pesquisa de satisfação para {nome} ({email})')")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar email para {nome} ({email}): {str(e)}")
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(5, null, {atendimento_concluido['id_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar email de pesquisa de satisfação para {nome} ({email}): {str(e)}')")
                continue

        return f"Pesquisas de Satisfação enviadas com sucesso! Quantidade: {len(atendimentos_concluídos)}"
    else:
        ontem = dt.today() - timedelta(days=1)
        print(f"[INFO] Nenhum atendimento concluído encontrado na data de {ontem}.")
        return f"Nenhum atendimento concluído encontrado na data de {ontem}."