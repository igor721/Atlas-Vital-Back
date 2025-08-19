from helpers.database import db
from models import Uf
import requests

def apiParaSql_UF_SQLAlchemy():
    print("Início da coleta de UFs via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    dados = requests.get(url).json()

    try:
        for uf in dados:
            regiao = uf.get('regiao', {})
            obj_uf = Uf.query.get(uf['id'])
            if obj_uf is None:
                obj_uf = Uf(
                    id=uf['id'],
                    sigla=uf['sigla'],
                    nome=uf['nome'],
                    regiao=regiao.get('nome', ''),
                    cod_regiao=regiao.get('id', None)
                )
                db.session.add(obj_uf)
        db.session.commit()
        print("Todas as UFs do Brasil foram inseridas com sucesso no banco.")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar UFs para banco: {e}")
