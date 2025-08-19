from helpers.database import db
from models import Mesorregiao
import requests

def apiParaSql_Mesorregiao_SQLAlchemy():
    print("Início da coleta de mesorregiões via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
    dados = requests.get(url).json()

    try:
        for meso in dados:
            uf = meso.get('UF', {})
            obj_meso = Mesorregiao.query.get(meso['id'])
            if obj_meso is None:
                obj_meso = Mesorregiao(
                    id=meso['id'],
                    nome=meso['nome'],
                    co_uf=uf.get('id')
                )
                db.session.add(obj_meso)
        db.session.commit()
        print("Mesorregiões inseridas com sucesso no banco.")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar mesorregiões para banco: {e}")
