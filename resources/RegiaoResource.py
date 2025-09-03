# Exemplo: RegiaoResource.py
from flask_restful import Resource
from models import Regiao
from flask import jsonify

class RegiaoResource(Resource):
    def get(self):
        regioes = Regiao.query.all()
        return jsonify([{"id": r.id, "sigla": r.sigla, "nome": r.nome} for r in regioes])
