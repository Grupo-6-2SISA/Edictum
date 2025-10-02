# MÓDULO DESATIVADO

"""
import os
from ics import Calendar, Event
from datetime import timedelta

def criar_arquivo_ics(titulo, descricao, inicio, duracao_minutos, local, nome_arquivo):
    # Caminho da pasta temp_ics na raiz do projeto
    pasta_temp = os.path.join(os.getcwd(), 'temp_ics')
    os.makedirs(pasta_temp, exist_ok=True)  # cria se não existir

    caminho_arquivo = os.path.join(pasta_temp, nome_arquivo)

    c = Calendar()
    e = Event()
    e.name = titulo
    e.begin = inicio
    e.duration = timedelta(minutes=duracao_minutos)
    e.description = descricao
    e.location = local
    c.events.add(e)

    with open(caminho_arquivo, 'w') as f:
        f.writelines(c)

    return caminho_arquivo
"""