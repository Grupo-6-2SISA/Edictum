import os
from core import database as db
from core.services import email_service as es
from datetime import datetime

def run():
    aniversariantes = db.executarSelect("SELECT *, CASE WHEN DATE_FORMAT(data_nascimento, '%m-%d') = DATE_FORMAT(CURDATE(), '%m-%d') THEN 1 ELSE 0 END AS eh_aniversario_hoje FROM cliente WHERE DATE_FORMAT(data_nascimento, '%m-%d') BETWEEN DATE_FORMAT(CURDATE(), '%m-%d') AND DATE_FORMAT(DATE_ADD(CURDATE(), INTERVAL 7 DAY), '%m-%d') AND cnpj IS NULL")

    emails = db.executarSelect("SELECT email FROM usuario WHERE is_ativo = 1 AND email IS NOT NULL")
    emails = [email['email'] for email in emails]  # Extrai os emails em uma lista

    if aniversariantes:
        mensagem = None
        for cliente in aniversariantes:
            nome_cliente = cliente['nome']
            email = emails
            data_aniversario = cliente['data_nascimento']
            data_formatada = data_aniversario.strftime('%d/%m')


            if cliente['eh_aniversario_hoje'] == 0:
                assunto = f"Aniversário de Cliente: {nome_cliente} em 7 dias"
                mensagem = f"""
                Prezado(a) colaborador(a),
    
                Gostaríamos de informar que o cliente {nome_cliente} fará aniversário no dia {data_formatada}, ou seja, em 7 dias.
                
                Essa é uma ótima oportunidade para reforçar o relacionamento com o cliente, enviando uma mensagem de felicitações ou oferecendo alguma atenção especial em nome do Escritório Orlando Matos Advogados Associados.
                
                Atenciosamente,  
                Equipe Orlando Matos Advogados Associados
                """
            elif cliente['eh_aniversario_hoje'] == 1:
                assunto = f"Aniversário de Cliente: {nome_cliente} - Hoje!"
                mensagem = f"""
                Prezado(a) colaborador(a),
    
                Gostaríamos de informar que o cliente {nome_cliente} está fazendo aniversário hoje ({data_formatada}).
                
                Essa é uma ótima oportunidade para reforçar o relacionamento com o cliente, enviando uma mensagem de felicitações ou oferecendo alguma atenção especial em nome do Escritório Orlando Matos Advogados Associados.
                
                Atenciosamente,  
                Equipe Orlando Matos Advogados Associados
                """
            try:
                es.enviar_email(destinatario=email, assunto=assunto, corpo=mensagem, bcc=[os.getenv('EMAIL_MONITOR')])
                db.executarQuery("INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                                 f"(null, {cliente['id_cliente']}, null, null, 1, DEFAULT, NOW(), 'Sucesso ao enviar email de lembrete de aniversário para {nome_cliente} para os funcionarios')")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar email para funcionarios, cliente: {nome_cliente} ({emails}): {str(e)}")
                db.executarQuery("INSERT INTO log_envio_lembrete (fk_atendimento, fk_cliente, fk_conta, fk_nota_fiscal, funcionou, id_log_envio_lembrete, data_hora_criacao, mensagem) VALUES "
                                 f"(null, {cliente['id_cliente']}, null, null, 0, DEFAULT, NOW(), 'Falha ao enviar email de lembrete de aniversário para {nome_cliente} para os funcionarios: {str(e)}')")
                continue
    else:
        print("[INFO] Nenhum aniversariante encontrado para hoje.")
        return