def run():
    raise RuntimeError("Erro proposital para teste")
python
import os
from core import database as db
from core.services import email_service as es

def run():
    clientes = db.executarSelect("""
        SELECT *
        FROM cliente
        WHERE is_ativo = 1
          AND data_inicio IS NOT NULL
          AND DATEDIFF(CURDATE(), data_inicio) = 365
          AND email IS NOT NULL
    """)

    if not clientes:
        print("[INFO] Nenhum cliente faz 1 ano de associação hoje.")
        return

    for cliente in clientes:
        nome_cliente = cliente['nome']
        data_inicio = cliente['data_inicio'].strftime('%d/%m/%Y')
        assunto = f"Parabéns pelo seu 1º ano de associação!"
        mensagem = f"""
        Prezado(a) {nome_cliente},

        Hoje celebramos o seu primeiro ano de associação conosco, iniciado em {data_inicio}!

        Agradecemos pela confiança e parceria. Conte sempre com o Escritório Orlando Matos Advogados Associados.

        Atenciosamente,
        Equipe Orlando Matos Advogados Associados
        """

        try:
            es.enviar_email(
                destinatario=[cliente['email']],
                assunto=assunto,
                corpo=mensagem,
                bcc=[os.getenv('EMAIL_MONITOR')]
            )
            db.executarQuery(
                "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                f"(4, null, {cliente['id_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar email de 1 ano de associação para {nome_cliente}')"
            )
        except Exception as e:
            print(f"[ERRO] Falha ao enviar email para cliente: {nome_cliente}: {str(e)}")
            erro_sql = str(e).replace("'", "''")
            db.executarQuery(
                "INSERT INTO log_envio_lembrete (fk_tipo_lembrete, fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                f"(4, null, {cliente['id_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar email de 1 ano de associação para {nome_cliente}: {erro_sql}')"
            )