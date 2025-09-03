from helpers.database import app, db

from extrator import (
    apiParaSql_UF_SQLAlchemy,
    atualizarEstatisticasUFs,
    apiParaSql_Mesorregiao_SQLAlchemy,
    apiParaSql_Microrregiao_SQLAlchemy,
    apiParaSql_Municipio_SQLAlchemy,
    atualizarEstatisticasMunicipios,
    apiParaSql_Regiao_SQLAlchemy
)

# colunas = [
#     "NO_ENTIDADE", "QT_MAT_BAS", "CO_ENTIDADE", "CO_MUNICIPIO", "NU_ANO_CENSO", "NO_REGIAO", 
# ]

# regioes_brasil = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
# arquivos_csv = [
#     "microdados_ed_basica_2023.csv",
#     "microdados_ed_basica_2024.csv"
# ]

with app.app_context():
    # apiParaSql_UF_SQLAlchemy()
    # atualizarEstatisticasUFs()
    # apiParaSql_Mesorregiao_SQLAlchemy()
    # apiParaSql_Microrregiao_SQLAlchemy()
    # apiParaSql_Municipio_SQLAlchemy()
    atualizarEstatisticasMunicipios()
    # apiParaSql_Regiao_SQLAlchemy()

  
print("Importação completa de todos os dados.")
