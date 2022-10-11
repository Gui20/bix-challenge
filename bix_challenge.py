from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import *
import requests
import pandas as pd
from sqlalchemy import create_engine

engine_solution = create_engine('postgresql://guilherme:|?7LXmg+FWL&,'
                                '2(@bix-solution.c3ksuxpujoxa.sa-east-1.rds.amazonaws.com/postgres')
engine = create_engine('postgresql://junior:|?7LXmg+FWL&,2(@34.173.103.16/postgres')
df = pd.read_sql(""" SELECT * FROM public.venda """, con=engine)


def funcionarios():
    engine_solution.execute(""" DELETE FROM auxiliar.funcionarios """)
    for i in sorted(df['id_funcionario'].unique()):
        try:
            resp = requests.get("https://us-central1-bix-tecnologia-prd.cloudfunctions.net"
                                "/api_challenge_junior?id={}".
                                format(i))
            engine_solution.execute("""INSERT INTO auxiliar.funcionarios (id, nome_funcionario) VALUES ('%s', 
            '%s') """ % (i, resp.text))

        except IndexError as e:
            engine_solution.execute("""INSERT INTO auxiliar.funcionarios (id, nome_funcionario) VALUES ('%s', 
                        '%s') """ % (i, i))


def categorias():
    df_cat = pd.read_parquet('https://storage.googleapis.com/challenge_junior/categoria.parquet', engine='pyarrow')
    df_cat.to_sql("categorias", schema="auxiliar", index=False, if_exists='replace', con=engine_solution)


def transform_load():
    funcionarios = pd.read_sql(""" SELECT * FROM auxiliar.funcionarios """, con=engine_solution)
    df_categoria = pd.read_sql(""" SELECT * FROM auxiliar.categorias """, con=engine_solution)

    for i, v in df.iterrows():
        df.loc[i, 'id_funcionario'] = funcionarios['nome_funcionario'][funcionarios['id'] == v['id_funcionario']][
            funcionarios['nome_funcionario'][
                funcionarios['id'] == v['id_funcionario']].index[0]]

        df.loc[i, 'id_categoria'] = df_categoria['nome_categoria'][df_categoria['id'] == v['id_categoria']][
            df_categoria['nome_categoria'][
                df_categoria['id'] == v['id_categoria']].index[0]]

    df.rename(columns={'id_funcionario': 'funcionario', 'id_categoria': 'categoria'}, inplace=True)
    df.to_sql("vendas_solution", con=engine_solution, if_exists='replace', index=False)


with DAG("bix_challenge",
         start_date=datetime(2022, 10, 8),
         schedule='@hourly',
         catchup=False) as dag:
    refresh_funcionarios = PythonOperator(
        task_id="funcionarios",
        python_callable=funcionarios
    )

    refresh_categorias = PythonOperator(
        task_id="categorias",
        python_callable=categorias
    )

    transf_l = PythonOperator(
        task_id="transform_load",
        python_callable=transform_load
    )

[refresh_funcionarios, refresh_categorias] >> transf_l
