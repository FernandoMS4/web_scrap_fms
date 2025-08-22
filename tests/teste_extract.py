from bs4 import BeautifulSoup as bs

htm = '<div class="ui-search-result__wrapper"><div class="poly-card poly-card--list poly-card--large poly-card--CORE">' \
'<div class="poly-card__portada"><img alt="Fritadeira Elétrica Air Fryer WAP Barbecue com Painel Digital e 12 Funções" aria-hidden="true" ' \
'class="poly-component__picture" decoding="sync" fetchpriority="high" ' \
'height="150" src="https://http2.mlstatic.com/D_Q_NP_2X_952581-MLU75357540145_032024-V.webp" ' \
'title="Fritadeira Elétrica Air Fryer WAP Barbecue com Painel Digital e 12 Funções" ' \
'width="150"/></div><div class="poly-card__content"><span class="poly-component__highlight"' \
' style="color:#FFFFFF;background-color:#333333">RECOMENDADO</span><h3 class="poly-component__title-wrapper">' \
'<a class="poly-component__title" ' \
'href="https://www.mercadolivre.com.br/fritadeira-eletrica-air-fryer-wap-barbecue-com-painel-digital-e-12-funcoes/p/MLB27773891#polycard_client=search-nordic&amp;searchVariation=MLB27773891&amp;wid=MLB3611252531&amp;position=3&amp;search_layout=stack&amp;type=product&amp;tracking_id=f477a3e3-5487-495c-89d3-0b15522ce970&amp;sid=search" ' \
'target="_self">Fritadeira Elétrica Air Fryer WAP Barbecue com Painel Digital e 12 Funções</a>' \
'</h3><span class="poly-component__seller">Por Mercado Livre <svg aria-label="Loja oficial" height="12" role="img" viewbox="0 0 12 12" width="12">' \
'<use href="#poly_cockade"></use></svg></span><div class="poly-content">' \
'<div class="poly-content__column"><div class="poly-component__price">' \
'<s aria-label="Antes: 1499 reais" aria-roledescription="Valor" class="andes-money-amount andes-money-amount--previous andes-money-amount--cents-comma" ' \
'role="img" style="font-size:12px"><span aria-hidden="true" ' \
'class="andes-money-amount__currency-symbol">R$</span>' \
'<span aria-hidden="true" class="andes-money-amount__fraction">1.499</span></s>' \
'<div class="poly-price__current"><span aria-label="Agora: 1133 reais" aria-roledescription="Valor" ' \
'class="andes-money-amount andes-money-amount--cents-superscript" role="img" ' \
'style="font-size:24px"><span aria-hidden="true" ' \
'class="andes-money-amount__currency-symbol">R$</span>' \
'<span aria-hidden="true" class="andes-money-amount__fraction">1.133</span>' \
'</span><span class="andes-money-amount__discount" style="font-size:14px">24% OFF</span>' \
'</div><span class="poly-price__installments" style="color:#00a650">10x <span aria-label="113 reais com 30 centavos" aria-roledescription="Valor" ' \
'class="andes-money-amount poly-phrase-price andes-money-amount--cents-comma" role="img" style="font-size:inherit"><span aria-hidden="true" ' \
'class="andes-money-amount__currency-symbol">R$</span><span aria-hidden="true" class="andes-money-amount__fraction">113</span>' \
'<span aria-hidden="true">,</span><span aria-hidden="true" class="andes-money-amount__cents">30</span>' \
'</span> sem juros</span></div><div class="poly-component__shipping"><span class="poly-shipping--next_day">Chegará grátis amanhã</span>' \
'</div><span class="poly-component__shipped-from">Enviado pelo <svg aria-label="FULL" height="13" role="img" viewbox="0 0 41 13" width="41">' \
'<use href="#poly_full"></use></svg></span></div><div class="poly-content__column"><div class="poly-component__reviews">' \
'<span class="andes-visually-hidden">Avaliação 4,9 de 5. (1.346 avaliações)</span><span aria-hidden="true" class="poly-reviews__rating">4.9</span>' \
'<span class="poly-reviews__starts"><svg aria-hidden="true" height="15" viewbox="0 0 15 15" width="15"><use href="#poly_star_fill"></use></svg> ' \
'<svg aria-hidden="true" height="15" viewbox="0 0 15 15" width="15"><use href="#poly_star_fill"></use></svg> ' \
'<svg aria-hidden="true" height="15" viewbox="0 0 15 15" width="15"><use href="#poly_star_fill"></use></svg> ' \
'<svg aria-hidden="true" height="15" viewbox="0 0 15 15" width="15"><use href="#poly_star_fill"></use></svg> ' \
'<svg aria-hidden="true" height="15" viewbox="0 0 15 15" width="15"><use href="#poly_star_fill"></use></svg>' \
'</span><span aria-hidden="true" class="poly-reviews__total">(1346)</span></div></div></div></div>' \
'<div class="poly-component__bookmark" data-testid="bookmark"><button aria-checked="false" aria-label="Favorito" class="poly-bookmark__btn" ' \
'role="switch" type="button"><svg class="poly-bookmark__icon-full" height="20" viewbox="0 0 20 20" width="20"><use href="#poly_bookmark"></use>' \
'</svg><svg class="poly-bookmark__icon-empty" height="20" viewbox="0 0 20 20" width="20"><use href="#poly_bookmark"></use></svg></button></div></div></div>'

soup = bs(htm)

reviews = soup.find(class_='poly-reviews__rating').text


reviews_qtd = soup.find(class_='poly-reviews__total').text


product_price_local = soup.find(class_='andes-money-amount__currency-symbol').text
print(product_price_local)

product_price_from = soup.find_all(class_ ='andes-money-amount__fraction')[0].text
print(product_price_from)

product_price_from_cents = '0'

product_price_to = soup.find_all(class_ ='andes-money-amount__fraction')[1].text
print(product_price_to)

product_price_to_cents = '0'

product_url = soup.find('a')['href']
print(product_url)

product_img = soup.find(class_='poly-component__picture')['src']
print(product_img)