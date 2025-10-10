FROM astrocrpublic.azurecr.io/runtime:3.0-2
EXPOSE 3306

COPY . /usr/local/airflow/

WORKDIR /usr/local/airflow/

RUN pip install --upgrade pip && pip install -r requirements.txt