from core import database as db
from core import task_loader as tl
import datetime as dt
import os

def main():
    exibir_banner()
    print(f"\n[INFO] APLICACAO INICIALIZADA - DATA E HORA: {dt.datetime.now()} ")

    rotinas = obter_rotinas_agendadas()

    if not rotinas:
        informar_sem_rotinas()
    else:
        executar_rotinas(rotinas)

    print(f"\n[INFO] APLICACAO FINALIZADA - DATA E HORA: {dt.datetime.now()} ")

def exibir_banner():
    print("""
    
        8 8888888888   8 888888888o.       8 8888     ,o888888o. 8888888 8888888888 8 8888      88        ,8.       ,8.         
        8 8888         8 8888    `^888.    8 8888    8888     `88.     8 8888       8 8888      88       ,888.     ,888.        
        8 8888         8 8888        `88.  8 8888 ,8 8888       `8.    8 8888       8 8888      88      .`8888.   .`8888.       
        8 8888         8 8888         `88  8 8888 88 8888              8 8888       8 8888      88     ,8.`8888. ,8.`8888.      
        8 888888888888 8 8888          88  8 8888 88 8888              8 8888       8 8888      88    ,8'8.`8888,8^8.`8888.     
        8 8888         8 8888          88  8 8888 88 8888              8 8888       8 8888      88   ,8' `8.`8888' `8.`8888.    
        8 8888         8 8888         ,88  8 8888 88 8888              8 8888       8 8888      88  ,8'   `8.`88'   `8.`8888.   
        8 8888         8 8888        ,88'  8 8888 `8 8888       .8'    8 8888       ` 8888     ,8P ,8'     `8.`'     `8.`8888.  
        8 8888         8 8888    ,o88P'    8 8888    8888     ,88'     8 8888         8888   ,d8P ,8'       `8        `8.`8888. 
        8 888888888888 8 888888888P'       8 8888     `8888888P'       8 8888          `Y88888P' ,8'         `         `8.`8888.

    """)


def obter_rotinas_agendadas():
    agora = dt.datetime.now()
    minuto_inicio = agora.replace(second=0, microsecond=0)
    minuto_fim = minuto_inicio + dt.timedelta(minutes=3)

    query = f"""
        SELECT *
        FROM Rotina
        WHERE hora_inicio >= '{minuto_inicio.strftime('%H:%M:%S')}'
          AND hora_inicio < '{minuto_fim.strftime('%H:%M:%S')}'
          AND (data_hora_ultima_execucao IS NULL OR data_hora_ultima_execucao < '{minuto_inicio.strftime('%Y-%m-%d')}')
    """

    return db.executarSelect(query)


def informar_sem_rotinas():
    print("[INFO] Nenhuma rotina agendada para o horário atual.")

def marcar_execucao(rotina_id):
    query = f"""
        UPDATE Rotina
        SET data_hora_ultima_execucao = NOW()
        WHERE id_rotina = {rotina_id}
    """
    db.executarQuery(query)


def executar_rotinas(rotinas):
    for rotina in rotinas:
        if rotina.get('is_ativo') < 1:
            registrar_rotina_bloqueada(rotina)
            continue

        tl.execute_task(rotina['rotina_chamada'], rotina)
        marcar_execucao(rotina['id_rotina'])
        logar_execucao(rotina['id_rotina'])

def registrar_rotina_bloqueada(rotina):
    db.executarQuery(
        "INSERT INTO log_execucao_rotina "
        "(fk_rotina, id_log_execucao_rotina, is_bloqueado, data_hora_ini_execucao, data_hora_fim_execucao, status_execucao) "
        f"VALUES ({rotina['id_rotina']}, DEFAULT, 1, NOW(), NOW(), 'Rotina Bloqueada, não executada.')"
    )

def logar_execucao(rotina_id):
    db.executarQuery(
        "INSERT INTO log_execucao_rotina "
        "(fk_rotina, id_log_execucao_rotina, is_bloqueado, data_hora_ini_execucao, data_hora_fim_execucao, status_execucao) "
        f"VALUES ({rotina_id}, DEFAULT, 0, NOW(), NOW(), 'Execução concluída.')"
    )


if __name__ == '__main__':
    main()
