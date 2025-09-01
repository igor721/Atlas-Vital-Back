from helpers.database import db
from models import Mesorregiao
import requests

def apiParaSql_Mesorregiao_SQLAlchemy():
    print("Início da coleta de mesorregiões via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
    resp = requests.get(url)
    
    if resp.status_code != 200:
        print(f"Erro ao acessar {url}: {resp.status_code}")
        return

    dados = resp.json()

    try:
        for meso in dados:
            uf = meso.get('UF', {})
            obj_meso = Mesorregiao.query.get(meso['id'])
            
            if obj_meso is None:
                obj_meso = Mesorregiao(
                    id=meso['id'],
                    nome=meso.get('nome', ''),
                    cod_uf=uf.get('id')
                )
                db.session.add(obj_meso)
            else:
                # Atualiza caso já exista
                obj_meso.nome = meso.get('nome', obj_meso.nome)
                obj_meso.co_uf = uf.get('id', obj_meso.co_uf)

        db.session.commit()
        print("Mesorregiões inseridas/atualizadas com sucesso no banco.")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar mesorregiões para banco: {e}")
