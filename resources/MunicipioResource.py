# resources/MunicipioResource.py
from flask_restful import Resource
from flask import jsonify
from models import Municipio

class MunicipioResource(Resource):
    def get(self):
        municipios = Municipio.query.all()
        return jsonify([
            {
                "id": m.id,
                "nome": m.nome,
                "cod_microrregiao": m.cod_microrregiao,
                "cod_uf": m.cod_uf  # adicionei cod_uf para facilitar filtro no frontend
            }
            for m in municipios
        ])
