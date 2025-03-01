import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs


def captura_produtos_mercado_livre(url: str):

    """
    Captura dados do Mercado Livre, recebendo uma url como parametro para realizar o parse no site e capturar os produtos.
    url = "https://example.com"

    """
    url1: str = url
    while url1 != '':
        response: str = requests.get(url1)
        if response.status_code == 200:
            soup = bs(response.text, 'html.parser')

            produtos = soup.find_all(
                'div',
                class_='andes-card poly-card poly-card--grid-card andes-card--flat andes-card--padding-0 andes-card--animated',
            )
            if produtos is None or produtos == []:
                produtos = soup.find_all(
                    'div', class_='poly-card poly-card--list'
                )

            next_url = soup.find(
                'li',
                class_='andes-pagination__button andes-pagination__button--next',
            )
            if next_url is None:
                url1 = ''
            else:
                url1 = next_url.find('a', href=True)['href']

            for produto in produtos:

                product_name = produto.find(
                    'a', class_='poly-component__title'
                )
                reviews = produto.find('span', class_='poly-reviews__rating')
                reviews_qtd = produto.find(
                    'span', class_='poly-reviews__total'
                )
                product_price_local = produto.find(
                    'span', class_='andes-money-amount__currency-symbol'
                )
                product_price_from = produto.find(
                    's',
                    class_='andes-money-amount andes-money-amount--previous andes-money-amount--cents-comma',
                )
                product_price_from_cents = '0'
                if product_price_from is not None:
                    product_price_from_cents = product_price_from.find(
                        'span', class_='andes-money-amount__cents'
                    )
                    if product_price_from_cents is not None:
                        product_price_from_cents = product_price_from.find(
                            'span', class_='andes-money-amount__cents'
                        ).text
                product_price_to = (
                    produto.find('div', class_='poly-price__current')
                    .find('span', class_='andes-money-amount__fraction')
                    .text
                )
                product_price_to_cents = produto.find(
                    'div', class_='poly-price__current'
                ).find('span', class_='andes-money-amount__cents')
                product_url = produto.find('a')['href']
                product_img = ''
                if (
                    'data:image'
                    in produto.find('img', class_='poly-component__picture')[
                        'src'
                    ]
                ):
                    product_img = produto.find(
                        'img', class_='poly-component__picture'
                    )['data-src']
                else:
                    product_img = produto.find(
                        'img', class_='poly-component__picture'
                    )['src']

                yield {
                    'product_name': None
                    if product_name is None
                    else product_name.get_text(strip=True),
                    'reviews': '0'
                    if reviews is None
                    else reviews.get_text(strip=True),
                    'reviews_qtd': '0'
                    if reviews_qtd is None
                    else reviews_qtd.get_text(strip=True),
                    'product_price_local': None
                    if product_price_local is None
                    else product_price_local.get_text(strip=True),
                    'product_price_from_fraction': '0'
                    if product_price_from is None
                    else product_price_from.find(
                        'span', class_='andes-money-amount__fraction'
                    ).get_text(strip=True),
                    'product_price_from_cents': '0'
                    if product_price_from_cents is None
                    else product_price_from_cents,
                    'product_price_to': product_price_to,
                    'product_price_to_cents': '0'
                    if product_price_to_cents is None
                    else product_price_to_cents.text,
                    'product_url': product_url,
                    'product_image': product_img,
                    'modified_date': datetime.now().strftime(
                        '%y-%m-%d %H:%M:%S'
                    ),
                }
    time.sleep(1)


if __name__ == '__main__':
    
    url = 'https://lista.mercadolivre.com.br/controle-sem-fio#D[A:controle%20sem%20fio]'
    
    print(captura_produtos_mercado_livre(url=url))
