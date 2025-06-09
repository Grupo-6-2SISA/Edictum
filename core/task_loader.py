# core/task_loader.py
import importlib
import time
from pathlib import Path
from core import database as db
from datetime import datetime
def execute_task(task_name: str, rotina: dict) -> bool:
    """
    Carrega e executa uma tarefa pelo nome

    Args:
        task_name: Nome do script (sem extensão .py)

    Returns:
        True se executado com sucesso, False caso contrário
    """
    # 1. Validação de segurança
    if not task_name.isidentifier():
        print(f"[ERRO] Nome de tarefa inválido: {task_name}")
        return False

    # 2. Verifica existência do arquivo
    task_path = Path(__file__).parent.parent / "tasks" / f"{task_name}.py"
    if not task_path.exists():
        print(f"[ERRO] Arquivo de tarefa não encontrado: {task_name}.py")
        return False

    start_time = None

    try:
        # 3. Importação dinâmica
        module = importlib.import_module(f"tasks.{task_name}")

        # 4. Verificação da interface
        if not hasattr(module, 'run'):
            print(f"[ERRO] Tarefa {task_name} não possui função 'run'")
            return False

        # 5. Execução cronometrada

        start_time = datetime.now()

        db.executarQuery(
            "INSERT INTO log_execucao_rotina (fk_rotina, id_log_execucao_rotina, is_bloqueado, data_hora_ini_execucao, status_execucao, funcionou) "
            f"VALUES ({rotina['id_rotina']}, DEFAULT, 0, '{start_time.strftime('%Y-%m-%d %H:%M:%S')}', 'Iniciando execução da tarefa {task_name}', null)"
        )

        print(f"[INFO] Iniciando execução da tarefa: {task_name}")
        retorno = module.run()  # Função principal da tarefa
        end_time = datetime.now()

        db.executarQuery(
            "INSERT INTO log_execucao_rotina (fk_rotina, id_log_execucao_rotina, is_bloqueado, data_hora_ini_execucao, data_hora_fim_execucao, status_execucao, funcionou) "
            f"VALUES ({rotina['id_rotina']}, DEFAULT, 0, '{start_time.strftime('%Y-%m-%d %H:%M:%S')}', '{end_time.strftime('%Y-%m-%d %H:%M:%S')}', 'Tarefa {task_name} executada com sucesso: {retorno}', 1)"
        )

        duration = (end_time - start_time).total_seconds()
        print(f"[INFO] Tarefa {task_name} executada com sucesso em {duration:.3f}s")
        return True

    except Exception as e:
        end_time = datetime.now()
        ini_exec = start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else end_time.strftime('%Y-%m-%d %H:%M:%S')
        fim_exec = end_time.strftime('%Y-%m-%d %H:%M:%S')
        erro_msg = str(e).replace("'", "''")
        db.executarQuery(
            "INSERT INTO log_execucao_rotina (fk_rotina, id_log_execucao_rotina, is_bloqueado, data_hora_ini_execucao, data_hora_fim_execucao, status_execucao, funcionou) "
            f"VALUES ({rotina['id_rotina']}, DEFAULT, 0, '{ini_exec}', '{fim_exec}', 'Erro na tarefa {task_name}: {erro_msg}', 0)"
        )
        print(f"[ERRO CRÍTICO] Falha na execução da tarefa {task_name}: {erro_msg}")
    return False
