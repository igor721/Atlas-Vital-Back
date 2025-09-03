from flask_restful import Resource
from models import UfEstatistica
from flask import jsonify

class UfEstatisticaResource(Resource):
    def get(self, uf_id, ano):
        stats = UfEstatistica.query.filter_by(cod_uf=uf_id, ano=ano).all()
        return jsonify([{
            "id": s.id,
            "cod_uf": s.cod_uf,
            "ano": s.ano,
            "total_nascimento": s.total_nascimento,
            "total_morte": s.total_morte,
            "total_casamento": s.total_casamento
        } for s in stats])
