# resources/MunicipioEstatisticaResource.py
from flask_restful import Resource
from flask import jsonify
from helpers.database import db
from models import MunicipioEstatistica, Municipio

class MunicipioEstatisticaResource(Resource):
    def get(self, uf_id, ano):
        stats = (
            db.session.query(MunicipioEstatistica)
            .join(Municipio, MunicipioEstatistica.cod_municipio == Municipio.id)
            .filter(Municipio.cod_uf == uf_id, MunicipioEstatistica.ano == ano)
            .all()
        )
        return jsonify([
            {
                "id": s.id,
                "cod_municipio": s.cod_municipio,
                "ano": s.ano,
                "total_nascimento": s.total_nascimento,
                "total_morte": s.total_morte,
                "total_casamento": s.total_casamento
            }
            for s in stats
        ])
