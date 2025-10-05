import os
from core import database as db
from core.services import email_service as es
from core.services import twilio_send_sms as sms

def run():
    dados = db.executarSelect("""
        SELECT
        C.id_cliente AS id_cliente_indicado,
        C.nome AS cliente_indicado,
        C.data_inicio AS data_inicio_indicado,
        I.id_cliente AS id_indicador,
        I.nome AS nome_indicador,
        I.email AS email_indicador,
        I.telefone AS telefone_indicador,
        A.id_atendimento,
        A.data_inicio AS data_inicio_atendimento,
        A.data_fim AS data_fim_atendimento
    FROM cliente C
    JOIN cliente I
        ON C.fk_indicador = I.id_cliente
    JOIN (
        -- Subquery para clientes com exatamente 1 atendimento
        SELECT fk_cliente, MIN(id_atendimento) AS id_atendimento
        FROM atendimento
        GROUP BY fk_cliente
        HAVING COUNT(*) = 1
    ) AS A_UNICO
        ON C.id_cliente = A_UNICO.fk_cliente
    JOIN atendimento A
        ON A.id_atendimento = A_UNICO.id_atendimento
    LEFT JOIN historico_status_agendamento H
        ON H.fk_atendimento = A.id_atendimento
    WHERE C.fk_indicador IS NOT NULL
      AND C.data_inicio = CURDATE()
    GROUP BY C.id_cliente, A.id_atendimento;
    """)

    if dados:
        for dado in dados:
            nome_indicador = dado['nome_indicador']
            nome_indicado = dado['cliente_indicado']
            email = dado['email_indicador']
            telefone = dado['telefone_indicador']
            mensagem_email = f"""
            Prezado(a) {nome_indicador},

            Gostaríamos de agradecer por indicar {nome_indicado} para o nosso escritório Orlando Matos Advogados Associados.  

            Sua confiança e recomendação são extremamente importantes para nós e nos ajudam a continuar oferecendo um atendimento de excelência.  

            Conte sempre conosco para o que precisar — é um privilégio tê-lo(a) como cliente.

            Com os melhores votos,

            Orlando Matos Advogados Associados
            """

            mensagem_sms = f"Olá, {nome_indicador}! Obrigado por indicar {nome_indicado} ao nosso escritório. Sua confiança é muito importante para nós! – Equipe Orlando Matos Advogados Associados."

            try:
                es.enviar_email(destinatario=email, assunto="Agradecemos a Indicação! | Orlando Matos Advogados Associados",
                                corpo=mensagem_email, bcc=[os.getenv('EMAIL_MONITOR')])
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(null, {dado['id_indicador']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar email de agradecimento de indicacao para {nome_indicador} ({email})')")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar email para {nome_indicador} ({email}): {str(e)}")
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(null, {dado['id_indicador']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar email de agradecimento de indicacao para {nome_indicador} ({email}): {str(e)}')")
            try:
                sms.enviar_sms(mensagem=mensagem_sms, destinatario=telefone)
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(null, {dado['id_indicador']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar sms de agradecimento de indicacao para {nome_indicador} ({telefone})')")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar email para {nome_indicador} ({email}): {str(e)}")
                db.executarQuery(
                    "INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                    f"(null, {dado['id_indicador']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar sms de agradecimento de indicacao para {nome_indicador} ({telefone}): {str(e)}')")
            continue

        return f"Agradecimentos de Indicacao enviados com sucesso! Quantidade: {len(dados)}"
    else:
        print("[INFO] Nenhum indicado encontrado para hoje.")
        return "Nenhum indicado encontrado para hoje."

