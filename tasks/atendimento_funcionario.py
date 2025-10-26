import os
from core import database as db
from core.services import email_service as es

def run():
    atendimentos = db.executarSelect("""
        SELECT a.*, c.nome AS nome_cliente
        FROM atendimento a
        JOIN cliente c ON a.fk_cliente = c.id_cliente
        WHERE a.should_enviar_email = 1
    """)

    emails_funcionarios = db.executarSelect("SELECT email FROM usuario WHERE is_ativo = 1 AND email IS NOT NULL")
    emails_funcionarios = [e['email'] for e in emails_funcionarios]

    if not atendimentos:
        print("[INFO] Nenhum atendimento para envio de e-mail.")
        return

    for atendimento in atendimentos:
        assunto = f"Atendimento pendente: {atendimento['descricao']}"
        mensagem = f"""
        Prezado(a) colaborador(a),

        O atendimento '{atendimento['descricao']}' para o cliente {atendimento['nome_cliente']} está pendente.

        Data de início: {atendimento['data_inicio'].strftime('%d/%m/%Y %H:%M')}
        Data de vencimento: {atendimento['data_vencimento'].strftime('%d/%m/%Y %H:%M')}
        Valor: R$ {atendimento['valor']:.2f}

        Atenciosamente,
        Equipe Orlando Matos Advogados Associados
        """

        try:
            es.enviar_email(
                destinatario=emails_funcionarios,
                assunto=assunto,
                corpo=mensagem,
                bcc=[os.getenv('EMAIL_MONITOR')]
            )
            db.executarQuery(
                "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                f"(1, {atendimento['id_atendimento']}, {atendimento['fk_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar e-mail de atendimento para os funcionários')"
            )
        except Exception as e:
            print(f"[ERRO] Falha ao enviar e-mail para funcionários: {str(e)}")
            erro_sql = str(e).replace("'", "''")
            db.executarQuery(
                "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                f"(1, {atendimento['id_atendimento']}, {atendimento['fk_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar e-mail de atendimento para funcionários: {erro_sql}')"
            )def run():
    raise RuntimeError("Erro proposital para teste")
