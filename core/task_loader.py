# core/task_loader.py
import importlib
import time
from pathlib import Path

def execute_task(task_name: str) -> bool:
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

    try:
        # 3. Importação dinâmica
        module = importlib.import_module(f"tasks.{task_name}")

        # 4. Verificação da interface
        if not hasattr(module, 'run'):
            print(f"[ERRO] Tarefa {task_name} não possui função 'run'")
            return False

        # 5. Execução cronometrada
        start_time = time.time()
        print(f"[INFO] Iniciando execução da tarefa: {task_name}")
        module.run()  # Função principal da tarefa
        duration = time.time() - start_time

        print(f"[INFO] Tarefa {task_name} executada com sucesso em {duration:.2f}s")
        return True

    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha na execução da tarefa {task_name}: {str(e)}")
        return False