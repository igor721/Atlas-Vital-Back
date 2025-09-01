from helpers.database import db
from models import Uf, UfEstatistica
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def apiParaSql_UF_SQLAlchemy():
    print("Início da coleta de UFs via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code != 200:
        print(f"Erro ao acessar {url}: {resp.status_code}")
        return

    dados = resp.json()

    try:
        for uf in dados:
            regiao = uf.get("regiao", {})
            obj_uf = Uf.query.get(uf["id"])
            if obj_uf is None:
                obj_uf = Uf(
                    id=uf["id"],
                    sigla=uf["sigla"],
                    nome=uf["nome"],
                    cod_regiao=regiao.get("id", None),
                )
                db.session.add(obj_uf)
            else:
                # atualiza nome/sigla caso tenha mudado
                obj_uf.sigla = uf.get("sigla", obj_uf.sigla)
                obj_uf.nome = uf.get("nome", obj_uf.nome)
                obj_uf.cod_regiao = regiao.get("id", obj_uf.cod_regiao)

        db.session.commit()
        print("UFs do IBGE inseridas/atualizadas com sucesso.")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar UFs: {e}")


def atualizarEstatisticasUFs():
    print("Início da coleta de estatísticas de UFs via API do Registro Civil.")

    anos = range(2015, 2026)
    tipos = {
        "total_nascimento": "https://transparencia.registrocivil.org.br/api/record/birth",
        "total_morte": "https://transparencia.registrocivil.org.br/api/record/death",
        "total_casamento": "https://transparencia.registrocivil.org.br/api/record/marriage",
    }

    ufs = Uf.query.all()
    sigla_para_uf = {uf.sigla: uf for uf in ufs}

    try:
        for ano in anos:
            print(f"\nProcessando ano {ano}...")

            # Cria uma estatística para cada UF e ano
            estatisticas = {}
            for uf in ufs:
                estat = UfEstatistica(
                    cod_uf=uf.id,
                    ano=ano,
                    total_nascimento=0,
                    total_morte=0,
                    total_casamento=0
                )
                db.session.add(estat)
                estatisticas[uf.sigla] = estat

            # Preenche os totais vindos da API
            for campo, base_url in tipos.items():
                url = f"{base_url}?start_date={ano}-01-01&end_date={ano}-12-31"
                resp = requests.get(url, headers=HEADERS)

                if resp.status_code != 200:
                    print(f"Erro ao acessar {url}: {resp.status_code}")
                    continue

                dados = resp.json().get("data", [])
                for item in dados:
                    sigla = item["name"].strip().upper()
                    total = item["total"]
                    if sigla in estatisticas:
                        setattr(estatisticas[sigla], campo, total)
                    else:
                        print(f"Sigla {sigla} não encontrada no banco.")

            db.session.commit()
            print(f"Estatísticas do ano {ano} salvas no banco.")

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar estatísticas de UFs: {e}")


if __name__ == "__main__":
    apiParaSql_UF_SQLAlchemy()
    atualizarEstatisticasUFs()
