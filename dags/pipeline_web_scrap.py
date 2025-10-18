import json
import os
from datetime import datetime

from airflow.decorators import dag, task

from include.fms_extract import captura_produtos_mercado_livre,get_product
from include.fms_load import inserir_dados_csv
from include.fms_transform import format_scrapy_mercado_livre
from include.fms_database_generate import lista_prods

@dag( 
        dag_id="webscrapping",
        description="minha etl pica",
        schedule="0 * *  * *",
        start_date=datetime(2025,2,26),
        catchup=False
)
def pipeline():

    @task
    def data_folder():
        if os.path.exists('data') == False:
            os.mkdir('data')
        if os.path.exists('data/archive') == False:
            os.mkdir('data/archive')
        if os.path.exists('data/files') == False:
            os.mkdir('data/files')

    @task
    def listas_prods():
        return lista_prods()

    @task
    def lista_html_produtos(lista_produtos:list):
        return get_product(lista_produtos)

    @task
    def captura_produto(lista:list):
        with open('data/files/produtos_teste.jsonl', 'a', encoding='utf-8') as file:
            for i in captura_produtos_mercado_livre(response_= lista):
                file.write(json.dumps(i, ensure_ascii=False) + '\n')

    @task
    def format_arquivo_jsonl():
        df = format_scrapy_mercado_livre(reprocess=False)
        return df
    
    @task
    def insercao_banco(df):
        inserir_dados_csv(df)

    t1 = data_folder()
    t2 = listas_prods()
    t3 = lista_html_produtos(t2)
    t4 = captura_produto(t3)
    t5 = format_arquivo_jsonl()
    t6 = insercao_banco(t5) 

    t1 >> t2 >> t3 >> t4 >> t5 >> t6

pipeline()