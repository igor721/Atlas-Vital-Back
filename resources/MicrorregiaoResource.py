from flask_restful import Resource
from models import Microrregiao
from flask import jsonify

class MicrorregiaoResource(Resource):
    def get(self):
        microrregioes = Microrregiao.query.all()
        return jsonify([{"id": m.id, "nome": m.nome, "cod_mesorregiao": m.cod_mesorregiao} for m in microrregioes])
