from airflow.decorators import dag,task
from include.fms_extract import captura_produtos_mercado_livre
from include.fms_transform import format_scrapy_mercado_livre
from include.fms_load import inserir_dados_csv
import os
import json
from datetime import datetime

@dag( 
        dag_id="webscrapping",
        description="minha etl pica",
        schedule="*/5 * * * *",
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
    def captura_produto():
        url = 'https://lista.mercadolivre.com.br/controle-sem-fio#D[A:controle%20sem%20fio]'
        with open('data/files/produtos_teste.jsonl', 'a', encoding='utf-8') as file:
          for i in captura_produtos_mercado_livre(url=url):
              file.write(json.dumps(i, ensure_ascii=False) + '\n')

    @task
    def format_arquivo_jsonl():
        df = format_scrapy_mercado_livre(reprocess=False)
        return df
    
    @task
    def insersao_banco(df):
        inserir_dados_csv(df)

    t1 = data_folder()
    t2 = captura_produto()
    t3 = format_arquivo_jsonl()
    t4 = insersao_banco(t3)

    t1 >> t2 >> t3 >> t4

pipeline()