import time
from contextlib import nullcontext
from gettext import NullTranslations
from core import database as db
import datetime as dt
import os

data = None

def main():
    inicializar_aplicacao()

def inicializar_aplicacao():
    data = dt.datetime.now()

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
    time.sleep(0.5)
    print(f" APLICACAO INICIALIZADA - DATA E HORA: {data} ")


if __name__ == '__main__':
    main()


