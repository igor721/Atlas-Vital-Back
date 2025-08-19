from helpers.database import db
from models import Municipio, MunicipioEstatistica, Uf
import requests
import time


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def apiParaSql_Municipio_SQLAlchemy():
    print("Início da coleta de municípios via API do IBGE.")

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code != 200:
        print(f"Erro ao acessar {url}: {resp.status_code}")
        return

    dados = resp.json()
    total_ignorados = 0

    try:
        for mun in dados:
            micro = mun.get("microrregiao")
            # Ignora municípios sem microrregião
            if micro is None:
                total_ignorados += 1
                continue

            meso = micro.get("mesorregiao") or {}
            uf = meso.get("UF")
            # Ignora municípios sem UF
            if uf is None:
                total_ignorados += 1
                continue

            id_mun = mun.get("id")
            nome_mun = mun.get("nome") or "SEM NOME"
            cod_micro = micro.get("id")
            cod_uf = uf.get("id")

            obj_mun = Municipio.query.get(id_mun)
            if obj_mun is None:
                obj_mun = Municipio(
                    id=id_mun,
                    nome=nome_mun,
                    cod_microrregiao=cod_micro,
                    cod_uf=cod_uf
                )
                db.session.add(obj_mun)
            else:
                obj_mun.nome = nome_mun
                obj_mun.cod_microrregiao = cod_micro
                obj_mun.cod_uf = cod_uf

        db.session.commit()
        print(f"Municípios do IBGE inseridos/atualizados com sucesso.")
        print(f"Total de municípios ignorados por falta de microrregião ou UF: {total_ignorados}")

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar municípios: {e}")


def atualizarEstatisticasMunicipios():
    print("Início da coleta de estatísticas de municípios via API do Registro Civil.")

    anos = range(2015, 2026)
    tipos = {
        "total_nascimento": "https://transparencia.registrocivil.org.br/api/record/birth",
        "total_morte": "https://transparencia.registrocivil.org.br/api/record/death",
        "total_casamento": "https://transparencia.registrocivil.org.br/api/record/marriage",
    }

    ufs = Uf.query.all()
    municipios = Municipio.query.all()

    # Mapear (UF -> municípios)
    municipios_por_uf = {uf.sigla: [m for m in municipios if m.cod_uf == uf.id] for uf in ufs}

    # Lista de requisições que falharam
    falhas = []

    try:
        for ano in anos:
            print(f"\nProcessando ano {ano}...")

            for uf in ufs:
                estatisticas = {}
                for mun in municipios_por_uf.get(uf.sigla, []):
                    estat = MunicipioEstatistica(
                        cod_municipio=mun.id,
                        ano=ano,
                        total_nascimento=0,
                        total_morte=0,
                        total_casamento=0
                    )
                    db.session.add(estat)
                    estatisticas[mun.nome.upper()] = estat

                for campo, base_url in tipos.items():
                    url = f"{base_url}?start_date={ano}-01-01&end_date={ano}-12-31&state={uf.sigla}"
                    sucesso = False
                    for tentativa in range(3):  # tenta até 3 vezes
                        try:
                            resp = requests.get(url, headers=HEADERS, timeout=10)
                            resp.raise_for_status()
                            dados_api = resp.json().get("data") or []
                            for item in dados_api:
                                nome = (item.get("name") or "").strip().upper()
                                total = item.get("total") or 0
                                if nome in estatisticas:
                                    setattr(estatisticas[nome], campo, total)
                            sucesso = True
                            break  # saiu do loop se deu certo
                        except requests.RequestException as e:
                            print(f"Tentativa {tentativa+1} falhou para {url}: {e}")
                            time.sleep(2)  # espera 2 segundos antes de tentar novamente

                    if not sucesso:
                        print(f"Falha definitiva na requisição: {url}")
                        falhas.append(url)

            db.session.commit()
            print(f"Estatísticas municipais do ano {ano} salvas no banco.")

        # Processar requisições que falharam no final
        if falhas:
            print("\nTentando processar requisições que falharam no final...")
            for url in falhas:
                try:
                    resp = requests.get(url, headers=HEADERS, timeout=10)
                    resp.raise_for_status()
                    print(f"Requisição bem-sucedida no retry final: {url}")
                except requests.RequestException as e:
                    print(f"Não foi possível processar {url} nem no retry final: {e}")

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar estatísticas de municípios: {e}")


if __name__ == "__main__":
    apiParaSql_Municipio_SQLAlchemy()
    atualizarEstatisticasMunicipios()
