import pandas as pd
import os
import re


def format_scrapy_mercado_livre(reprocess: bool) -> bool:
    """
    Lê o arquivo coletado json e realiza o tratamento dos dados e padroniza de acordo com a tabela de produtos \n
    reprocess = True or False

    """
    if reprocess == False:
        try:
            df: pd.DataFrame = pd.read_json(
                'data/files/produtos_teste.jsonl',
                dtype='str',
                lines=True,
            )
        except KeyError as e:
            return print(f'Não foi possível ler o arquivo: {e}')
    elif reprocess == True:
        try:
            files: list = [f for f in os.listdir('data/archive/')]
            df: pd.DataFrame = pd.DataFrame()
            for i in files:
                df_concat = pd.read_json(
                    f'archive/{i}', dtype='str', lines=True
                )
                df = pd.concat([df, df_concat])
        except KeyError as e:
            print(f'Arquivos não encontrados {e} : {files}')

    df = df.sort_values(by=['product_name', 'modified_date'])

    df = df.drop_duplicates()

    df['reviews'] = df['reviews'].astype('float')

    df['reviews_qtd'] = (
        df['reviews_qtd']
        .str.replace('(', ' ')
        .str.replace(')', ' ')
        .astype('int')
    )

    df['product_price_from'] = (
        df['product_price_from_fraction'].astype('str').str.replace('.', '')
        + '.'
        + df['product_price_from_cents'].astype('str')
    ).astype('float')

    df['product_price_to'] = (
        df['product_price_to'].astype('str').str.replace('.', '')
        + '.'
        + df['product_price_to_cents'].astype('str')
    ).astype('float')

    df['marketplace'] = 'mercado livre'
    
    df['product_id'] = df['product_url'].str.replace('-','').apply(lambda url: re.search(r"MLB(\d+)", url).group(1) if re.search(r"MLB(\d+)", url) else '').astype('string')
    
    df = df[(df['product_id'] != '')]

    df = df.drop(
        columns=[
            'product_price_from_fraction',
            'product_price_from_cents',
            'product_price_to_cents',
        ]
    )
    return df


if __name__ == '__main__':
    # df = format_scrapy_amazon()
    # df.to_csv('data/dados_tratados.csv', header=True, index=False)
    df = format_scrapy_mercado_livre(reprocess=False)
    print(df)
