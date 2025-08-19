from helpers.database import db
from models import Microrregiao
import requests

def apiParaSql_Microrregiao_SQLAlchemy():
    print("Início da coleta de microrregiões via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
    dados = requests.get(url).json()

    try:
        for micro in dados:
            meso = micro.get('mesorregiao', {})
            uf = meso.get('UF', {})

            # Verifica se a microrregião já existe
            obj_micro = Microrregiao.query.get(micro['id'])

            if obj_micro is None:
                obj_micro = Microrregiao(
                    id=micro['id'],
                    nome=micro['nome'],
                    co_mesorregiao=meso.get('id'),
                    co_uf=uf.get('id')
                )
                db.session.add(obj_micro)

        db.session.commit()
        print("Microrregiões inseridas com sucesso no banco.")

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar microrregiões para o banco: {e}")
