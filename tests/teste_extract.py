import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import os
import mysql.connector
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def lista_prods():
    "Lista todos os produtos cadastrados para coleta"

    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    
    cur = conn.cursor()

    print("Iniciando captura de produtos")

    cur.execute("select product_name from web_scraping.market_place_search_products")

    print("Montando arquivo final")
    final = [i[0] for i in cur.fetchall()]
    print("Processo finalizado")
    return final

def captura_produtos_mercado_livre(url: str):

    """
    Captura dados do Mercado Livre, recebendo uma url como parametro para realizar o parse no site e capturar os produtos.
    url = "https://example.com"

    """
    session = requests.Session()
    session.headers.update(headers)

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
        return


    time.sleep(1)

    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        
        produtos = soup.find_all(
            'li',
            class_='ui-search-layout__item',
        )

        if not produtos:
            raise("Não foi possível encontrar produtos")
        for produto in produtos:
            product_name = produto.find('img')['title']
            
            if produto.find(class_='poly-reviews__rating'):
                reviews = produto.find(class_='poly-reviews__rating').text
            else:
                reviews = None
            if produto.find(class_='poly-reviews__total'):
                reviews_qtd = produto.find(class_='poly-reviews__total').text
            else: 
                reviews_qtd = None
            
            #print(reviews_qtd)
            
            if produto.find(class_='andes-money-amount__currency-symbol'):
                product_price_local = produto.find(class_='andes-money-amount__currency-symbol').text
            else:
                product_price_local = None
            #print(product_price_local)
            if produto.find_all(class_ ='andes-money-amount__fraction'):
                product_price_from = produto.find_all(class_ ='andes-money-amount__fraction')[0].text
            else:
                product_price_from = None    
            #print(product_price_from)
            product_price_from_cents = '0'
            if produto.find_all(class_ ='andes-money-amount__fraction'):
                product_price_to = produto.find_all(class_ ='andes-money-amount__fraction')[1].text
            else:
                product_price_to = None
            #print(product_price_to)
            product_price_to_cents = '0'
            if produto.find('a')['href']:
               product_url = produto.find('a')['href']
            else:
                product_url = None
            #print(product_url)
            if produto.find(class_='poly-component__picture'):
                product_img = produto.find(class_='poly-component__picture')['src']
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

    else:
        raise(f"Não foi possível realizar a coleta: status[{response.status_code}]")
   
    time.sleep(1)

if __name__ == "__main__":
    print("oi")
    print(lista_prods())
