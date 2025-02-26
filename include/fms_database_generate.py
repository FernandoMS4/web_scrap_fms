
from time import sleep
from sqlalchemy.dialects.mysql import insert,TEXT
from sqlalchemy.orm import declarative_base,Session
from sqlalchemy import String,Column,Text,Float,Integer,DateTime,TIMESTAMP,text,ForeignKey
from sqlalchemy import create_engine
import mysql.connector
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())


def get_env(key, default=None):
    value = os.getenv(key)
    return default if value is None else value


DB_HOST = get_env('DB_HOST')
DB_USER = get_env('DB_USER')
DB_PASSWORD = get_env('DB_PASSWORD')
DB_PORT = get_env('DB_PORT')
DB_NAME = get_env('DB_NAME')

"""
Variaveis
"""

mysql_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'


"""
Tabelas
"""

Base = declarative_base()

class Products(Base):
    """
    Esta tabela serve para armazenar os produtos
    """
    __tablename__ = 'products'
    product_id = Column(String(100), primary_key=True)
    product_name = Column(String(255), nullable=False)
    reviews = Column(Float, nullable=True)
    reviews_qtd = Column(Integer, nullable=True)
    product_price_local = Column(String(25), nullable=True)
    product_price_from = Column(Float, nullable=True)
    product_price_to = Column(Float, primary_key=True)
    created_date = Column(DateTime, default=datetime.now)
    modified_date = Column(DateTime, onupdate=datetime.now, nullable=True)
    marketplace = Column(String(50), primary_key=True)
    product_url = Column(Text, nullable=True)  # Melhor para URLs longas
    product_image = Column(Text, nullable=True)


class Market_Places(Base):
    """
    Tabela responsável por armazenar os market places disponíveis para captura
    """
    __tablename__ = 'marketplaces'
    id: str = Column(String(100),default=None, primary_key=True)
    marketplace_name = Column(String(25),nullable=False)


class Market_Place_Search_Products(Base):
    __tablename__ = 'market_place_search_products'
    id: int = Column(Integer,default=None, primary_key=True)
    brand: str = Column(String(25))
    product_name: str = Column(String(100))


class Status_User(Base):
    __tablename__ = 'status_user'
    id: int = Column(Integer,default=None, primary_key=True)
    name: str = Column(String(40))
    created_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'), 
        nullable=False
    )
    updated_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now,
        )


class Role(Base):
    __tablename__ = 'role'
    id: int = Column(Integer,default=None, primary_key=True)
    name: str = Column( String(40), nullable=False)
    create_at: datetime = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            onupdate=datetime.now,
            nullable=False)


class Users(Base):
    __tablename__ = 'users'
    id: int = Column(Integer,default=None, primary_key=True)
    name: str = Column(String(100), nullable=False)
    email: str = Column(String(70),default=None, nullable=True)
    password: str = Column(String(40),default=None, nullable=True)
    create_at: datetime = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            onupdate=datetime.now,
            nullable=False,
        )
    status_id = Column(
        Integer, 
        ForeignKey("status_user.id"),  # Correção aqui
        nullable=False,
        default=1  # Só use se garantir que sempre haverá um `status_user.id = 1`
    )
    email_confirmed: bool = Column(Float,default=None, nullable=True)
    hash_email_confirm: str = Column(String(80),default=None, nullable=True)


class StatusUser(Base):
    __tablename__ = 'statususer'
    id: int = Column(Integer,default=None, primary_key=True)
    name: str = Column(String(40))
    create_at: datetime = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False
        )
    updated_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now,
        )


class Roles(Base):
    __tablename__ = 'roles'
    id: int = Column(Integer,default=None, primary_key=True)
    name: str = Column(String(40))
    create_at: datetime = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False
    )
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now,
    )


class User(Base):
    __tablename__ = 'user'
    id: int = Column(Integer,default=None, primary_key=True)
    name: str = Column(String(100))
    email: str = Column(String(70),default=None)
    password: str = Column(String(40),default=None)
    create_at: datetime = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False
    )
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now,
        )
    status_id: int = Column(Integer,ForeignKey('status_user.id'), default=1)
    email_confirmed: bool = Column(Float,default=None)
    hash_email_confirm: str = Column(String(20),default=None)


class Roles_Users(Base):
    __tablename__ = 'roles_users'
    user_id: int = Column(Integer,ForeignKey('users.id'), primary_key=True)
    role_id: int = Column(Integer,ForeignKey('roles.id'), primary_key=True)


class Tokens(Base):
    __tablename__ = 'tokens'
    token: str = Column(String(255),primary_key=True)
    refresh_token: str = Column(String(255))
    expiration: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer,ForeignKey('users.id'))


class Hash_Tokens_Password(Base):
    __tablename__ = 'hash_tokens_password'
    token: str = Column(String(255),primary_key=True)
    expiration: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer,ForeignKey('users.id'))


class Genders(Base):
    __tablename__ = 'genders'
    id: int = Column(Integer,default=None, primary_key=True)
    name: str = Column(String(40))
    create_at: datetime = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False
    )
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now
    )


class User_Details(Base):
    __tablename__ = 'user_details'
    id: int = Column(Integer,default=None, primary_key=True)
    birth_date: datetime = Column(TIMESTAMP)
    create_at: datetime = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now
    )
    user_id: int = Column(Integer,ForeignKey('users.id'))
    gender_id: int = Column(Integer,ForeignKey('genders.id'))
    gender_additional_details: str = Column(String(70),
        default=None
    )


class Addresses(Base):
    __tablename__ = 'addresses'
    id: int = Column(Integer,default=None, primary_key=True)
    number: str = Column( String(12),default=None)
    street: str = Column(String(70))
    neighborhood: str = Column(String(50),default=None)
    state: str = Column(String(40),default=None)
    country: str = Column(String(70),default=None)
    cep: str = Column(String(12),default=None)
    additional_address_details: str = Column(String(40),default=None)
    lat: float = Column(Float,default=None)
    lng: float = Column(Float,default=None)
    city: str = Column(String(100),default=None)
    create_at: datetime = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False
    )
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now,
        )



class Addresses_User_Details(Base):
    __tablename__ = 'adresses_user_details'
    user_detail_id: int = Column(Integer,default=None, primary_key=True)
    address_id: int = Column(Integer,ForeignKey('addresses.id'))


class Email_Templates(Base):
    __tablename__ = 'email_templates'
    id: int = Column(Integer,default=None, primary_key=True)
    message: str = Column(TEXT)
    template_identifier: str = Column(String(30))
    create_at: datetime = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False
    )
    update_at: datetime = Column(
            TIMESTAMP,
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
            onupdate=datetime.now,
    )

class Settings(Base):
    __tablename__ = 'settings'
    id: int = Column(Integer,primary_key=True)
    expiration_token_hours: int = Column(Integer,default=2)

def create_engine_db():
    engine = create_engine(mysql_url)
    Base.metadata.create_all(engine)
    return engine


def verificar_database():
    """
    Função que verifica se o database existe no ambiente e o cria caso não exista\n
    Variaveis passadas no  arquivo .env conforme necessidade\n
    Connector: MysqlConnector

    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD
        )
        cursor = connection.cursor()

        cursor.execute(f"show databases like '{DB_NAME}'")
        result = cursor.fetchone()

        if not result:
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"Banco de dados '{DB_NAME}' criado com sucesso.")
        else:
            pass
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f'Erro ao verificar/criar o banco de dados: {err}')

if __name__ == '__main__':
    verificar_database()
    sleep(3)
    create_engine_db()