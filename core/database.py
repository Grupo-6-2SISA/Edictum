import os
from dotenv import load_dotenv
from mysql.connector import connect, Error
from pathlib import Path

# Arquivo de Configuração do Banco de Dados
''' Serve Duas Funções:
    - executarQuery(): Executa Qualquer Coisa que Não seja SELECT
    - executarSelect(): Executa APENAS SELECTs
 '''

# Carrega as variáveis de ambiente do arquivo .env
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

# Dicionário de Configuração do banco de dados, usado nas duas funções
config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DATABASE")
}

prod = os.getenv("PROD")

def executarQuery(script):
    """
    Função responsável por inserir os dados no banco.
    Recebe uma query SQL como parâmetro e a executa, usando as credenciais específicas.
    """
    db = None
    cursor = None
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.get_server_info()
            if not prod:
                print('Connected to MySQL server version -', db_info)

            cursor = db.cursor()
            if not prod:
                print(f"Executando a query: {script}")
            cursor.execute(script)
            db.commit()  # Confirma a transação no banco de dados
            print("Dados inseridos com sucesso!")

    except Error as e:
        print('Erro do MySQL (NAO-SELECT) -', e)

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def executarSelect(script):
    """
    Executa uma query SELECT e retorna os resultados como uma lista de dicionários.
    Cada dicionário representa uma linha, com os nomes das colunas como chaves.
    """
    db = None
    cursor = None
    rows = None
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.get_server_info()
            if not prod:
                print('Connected to MySQL server version -', db_info)

            cursor = db.cursor()
            if not prod:
                print(f"Executando o select: {script}")
            cursor.execute(script)

            colunas = [desc[0] for desc in cursor.description]  # nomes das colunas
            rows = [dict(zip(colunas, row)) for row in cursor.fetchall()]  # monta lista de dicionários

            if not prod:
                for row in rows:
                    print(row)

    except Error as e:
        print('Error do MySQL (SELECT) -', e)

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return rows