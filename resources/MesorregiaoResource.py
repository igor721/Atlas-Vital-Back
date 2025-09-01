from flask_restful import Resource
from models import Mesorregiao
from helpers.database import db
from flask import jsonify

class MesorregiaoResource(Resource):
    def get(self):
        mesorregioes = Mesorregiao.query.all()
        return jsonify([{"id": m.id, "nome": m.nome, "cod_uf": m.cod_uf} for m in mesorregioes])
