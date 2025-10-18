import time
from datetime import datetime
import json
import os

import requests
from bs4 import BeautifulSoup as bs




def get_product(produtos:list) :

    """
    Captura dados do Mercado Livre, recebendo uma url como parametro para realizar o parse no site e capturar os produtos.
    url = "https://example.com"

    """
    responses = []

    for i in produtos:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        session = requests.Session()
        session.headers.update(headers)
        url = f'https://lista.mercadolivre.com.br/{i}?sb=all_mercadolibre'

        try:
            print("Iniciando a requisição")
            time.sleep(1)
            response = session.get(url, timeout=10,allow_redirects=False)

            location = response.headers.get("Location")

            print(f"Status da requisição: {response.status_code}\n")
            print(f"Redirecionado para: {location}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Erro na requisição:", e)
            pass
        responses.append(response.text)

    return responses

def captura_produtos_mercado_livre(response_=list):

    """
    Transforma os dados coletados e oganiza os dados retornando um arquivo JSONL
    """

    if len(response_) > 0:
        for resp in response_:
            soup = bs(resp, 'html.parser')
            
            produtos = soup.find_all(
                'li',
                class_='ui-search-layout__item',
            )

            if not produtos:
                raise("Não foi possível encontrar produtos")
            for produto in produtos:
                product_name = produto.find('img')['title']
                
                if produto.find(class_='poly-reviews__rating'):
                    try:
                        reviews = produto.find(class_='poly-reviews__rating').text
                    except:
                        pass
                else:
                    reviews = None
                if produto.find(class_='poly-reviews__total'):
                    try:
                        reviews_qtd = produto.find(class_='poly-reviews__total').text
                    except:
                        pass
                else: 
                    reviews_qtd = None       
                #print(reviews_qtd)
                if produto.find(class_='andes-money-amount__currency-symbol'):
                    try:
                        product_price_local = produto.find(class_='andes-money-amount__currency-symbol').text
                    except:
                        pass
                else:
                    product_price_local = None
                #print(product_price_local)
                if produto.find_all(class_ ='andes-money-amount__fraction'):
                    try:
                        product_price_from = produto.find_all(class_ ='andes-money-amount__fraction')[0].text
                    except:
                        pass
                else:
                    product_price_from = None    
                #print(product_price_from)
                product_price_from_cents = '0'
                if produto.find_all(class_ ='andes-money-amount__fraction'):
                    try:
                        product_price_to = produto.find_all(class_ ='andes-money-amount__fraction')[1].text
                    except:
                        pass
                else:
                    product_price_to = None
                #print(product_price_to)
                product_price_to_cents = '0'
                if produto.find('a')['href']:
                    try:
                        product_url = produto.find('a')['href']
                    except:
                        pass
                else:
                    product_url = None
                #print(product_url)
                
                if produto.find(class_='poly-component__picture'):
                    if produto.find(class_='poly-component__picture') and 'data:image' not in produto.find(class_='poly-component__picture')['src']:
                        product_img = produto.find(class_='poly-component__picture')['src']
                if  produto.find(class_='poly-card__portada'):
                    try:
                        imagem = produto.find(class_='poly-card__portada').find('img')
                        product_img = imagem['data-src']
                    except:
                        pass
                else:
                    product_img = None
                #print(product_img)
                yield {
                    'product_name': product_name or None,
                    'reviews': reviews or "0",
                    'reviews_qtd': reviews_qtd or "0",
                    'product_price_local': product_price_local or None,
                    'product_price_from_fraction': product_price_from or "0",
                    'product_price_from_cents': product_price_from_cents or "0",
                    'product_price_to': product_price_to or None,
                    'product_price_to_cents': product_price_to_cents or "0",
                    'product_url': product_url,
                    'product_image': product_img,
                    'modified_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

            time.sleep(1)
        else:
             pass
    else:
        raise("A lista de produtos é vazia")

if __name__ == '__main__':

    print("oi")
    # produto = get_product(['climatizador-de-ar-wap-air-protect-135w'])

    # produtos = captura_produtos_mercado_livre(produto)

    # print(produtos)

    # for produto in produtos:
    # if produto.find(class_='poly-component__picture') and 'data:image' not in produto.find(class_='poly-component__picture')['src']:
    #     print('Primeiro')
    #     print(produto.find(class_='poly-component__picture')['src'])
    # if  produto.find(class_='poly-card__portada'):
    #     print('Segundo')
    #     print(produto.find(class_='poly-card__portada').find('img')['data-src'])