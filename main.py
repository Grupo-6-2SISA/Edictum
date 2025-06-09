import time
from contextlib import nullcontext
from gettext import NullTranslations
from core import database as db
from core import task_loader as tl
import datetime as dt
import os

data = None

def main():
    inicializar_aplicacao()

def inicializar_aplicacao():

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
    print(f"\n[INFO] APLICACAO INICIALIZADA - DATA E HORA: {dt.datetime.now()} ")

    rotinas = db.executarSelect("SELECT * FROM Rotina")

    for rotina in rotinas:

        if rotina['is_ativo'] != 1:
            db.executarQuery(
                f"INSERT INTO log_execucao_rotina (fk_rotina, id_log_execucao_rotina, is_bloqueado, data_hora_ini_execucao, data_hora_fim_execucao, status_execucao)"
                f" VALUES ({rotina['id_rotina']}, DEFAULT, 1, NOW(), NOW(), 'Rotina Bloqueada, não executada.')"
            )
            continue

        tl.execute_task(rotina['rotina_chamada'], rotina)

    print(f"\n[INFO] APLICACAO FINALIZADA - DATA E HORA: {dt.datetime.now()} ")

if __name__ == '__main__':
    main()


