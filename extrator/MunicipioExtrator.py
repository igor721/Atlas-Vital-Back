from helpers.database import db
from models import Municipio
import requests

def apiParaSql_Municipio_SQLAlchemy():
    print("Início da coleta de municípios via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    dados = requests.get(url).json()

    try:
        for municipio in dados:
            microrregiao = municipio.get('microrregiao')
            if microrregiao is None:
                continue  # pular se microrregiao não existir

            mesorregiao = microrregiao.get('mesorregiao')
            if mesorregiao is None:
                continue  # pular se mesorregiao não existir

            uf = mesorregiao.get('UF')
            if uf is None:
                continue  # pular se uf não existir

            co_uf = uf.get('id')
            if co_uf is None:
                continue

            obj_municipio = Municipio.query.get(municipio['id'])
            if obj_municipio is None:
                obj_municipio = Municipio(
                    id=municipio['id'],
                    nome=municipio['nome'],
                    co_uf=co_uf,
                    co_mesorregiao=mesorregiao.get('id'),
                    co_microrregiao=microrregiao.get('id')
                )
                db.session.add(obj_municipio)

        db.session.commit()
        print("Municípios inseridos com sucesso no banco.")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar municípios para banco: {e}")
