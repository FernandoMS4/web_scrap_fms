from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from .fms_database_generate import create_engine_db,Products



def inserir_dados_csv(dtframe):
    engine = create_engine_db()
    with Session(engine) as session:
        dados = []
        for _, linha in dtframe.iterrows():
            dados.append({
                "product_id": linha['product_id'],
                "product_name": linha['product_name'],
                "reviews": linha['reviews'],
                "reviews_qtd": linha['reviews_qtd'],
                "product_price_local": linha['product_price_local'],
                "product_price_from": linha['product_price_from'],
                "product_price_to": linha['product_price_to'],
                "modified_date": linha['modified_date'],
                "marketplace": linha['marketplace'],
                "product_url": linha['product_url'],
                "product_image": linha['product_image'],
            })

        insercoes = insert(Products).values(dados)

        insercoes = insercoes.on_duplicate_key_update(
            product_name=insercoes.inserted.product_name,
            reviews=insercoes.inserted.reviews,
            reviews_qtd=insercoes.inserted.reviews_qtd,
            product_price_local=insercoes.inserted.product_price_local,
            product_price_from=insercoes.inserted.product_price_from,
            product_price_to=insercoes.inserted.product_price_to,
            modified_date=insercoes.inserted.modified_date,
            marketplace=insercoes.inserted.marketplace,
            product_url=insercoes.inserted.product_url,
            product_image=insercoes.inserted.product_image,
        )
        session.execute(insercoes)
        session.commit()
        print('Dados inseridos com sucesso!')