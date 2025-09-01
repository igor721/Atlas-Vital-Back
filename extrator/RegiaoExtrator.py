from helpers.database import db
from models import Regiao
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def apiParaSql_Regiao_SQLAlchemy():
    print("Início da coleta de Regiões via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes"
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code != 200:
        print(f"Erro ao acessar {url}: {resp.status_code}")
        return

    dados = resp.json()

    try:
        for regiao in dados:
            obj_regiao = Regiao.query.get(regiao['id'])
            if obj_regiao is None:
                obj_regiao = Regiao(
                    id=regiao['id'],
                    sigla=regiao.get('sigla', ''),
                    nome=regiao.get('nome', '')
                )
                db.session.add(obj_regiao)
            else:
                obj_regiao.sigla = regiao.get('sigla', obj_regiao.sigla)
                obj_regiao.nome = regiao.get('nome', obj_regiao.nome)

        db.session.commit()
        print("Todas as Regiões do Brasil foram inseridas/atualizadas com sucesso no banco.")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar Regiões para banco: {e}")