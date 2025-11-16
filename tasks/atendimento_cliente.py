import os
from core import database as db
from core.services import email_service as es

def run():
    atendimentos = db.executarSelect("""
        SELECT a.*, u.email, c.nome AS nome_cliente
        FROM atendimento a
        JOIN usuario u ON a.fk_usuario = u.id_usuario
        JOIN cliente c ON a.fk_cliente = c.id_cliente
        WHERE a.should_enviar_email = 1
          AND u.is_ativo = 1
          AND u.email IS NOT NULL
          AND DATE(a.data_inicio) = DATE(NOW());
    """)

    if not atendimentos:
        print("[INFO] Nenhum atendimento para envio de e-mail.")
        return

    for atendimento in atendimentos:
        assunto = f"Atendimento hoje: {atendimento['nome_cliente']}"
        mensagem = f"""
        Prezado(a) cliente,

        Você tem um atendimento agendado para hoje!

        Data de início: {atendimento['data_inicio'].strftime('%d/%m/%Y %H:%M')}

        Atenciosamente,
        Equipe Orlando Matos Advogados Associados
        """

        try:
            es.enviar_email(
                destinatario=[atendimento['email']],
                assunto=assunto,
                corpo=mensagem,
                bcc=[os.getenv('EMAIL_MONITOR')]
            )
            db.executarQuery(
                "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                f"(3, {atendimento['id_atendimento']}, {atendimento['fk_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar e-mail de atendimento para o usuário {atendimento['fk_usuario']}')"
            )
        except Exception as e:
            print(f"[ERRO] Falha ao enviar e-mail para usuário {atendimento['fk_usuario']}: {str(e)}")
            erro_sql = str(e).replace("'", "''")
            db.executarQuery(
                "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                f"(3, {atendimento['id_atendimento']}, {atendimento['fk_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar e-mail de atendimento: {erro_sql}')"
            )