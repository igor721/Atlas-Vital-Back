from helpers.database import db
from models import Microrregiao
import requests

def apiParaSql_Microrregiao_SQLAlchemy():
    print("Início da coleta de microrregiões via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
    resp = requests.get(url)
    
    if resp.status_code != 200:
        print(f"Erro ao acessar {url}: {resp.status_code}")
        return

    dados = resp.json()

    try:
        for micro in dados:
            meso = micro.get('mesorregiao', {})

            # Verifica se a microrregião já existe
            obj_micro = Microrregiao.query.get(micro['id'])

            if obj_micro is None:
                obj_micro = Microrregiao(
                    id=micro['id'],
                    nome=micro.get('nome', ''),
                    cod_mesorregiao=meso.get('id')
                )
                db.session.add(obj_micro)
            else:
                # Atualiza caso já exista
                obj_micro.nome = micro.get('nome', obj_micro.nome)
                obj_micro.co_mesorregiao = meso.get('id', obj_micro.co_mesorregiao)

        db.session.commit()
        print("Microrregiões inseridas/atualizadas com sucesso no banco.")

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar microrregiões para o banco: {e}")
