from flask_restful import Resource
from flask import request, jsonify
from models import Uf

class UfResource(Resource):
    def get(self):
        regiao_id = request.args.get('regiao_id')
        if regiao_id and regiao_id.lower() != 'todas':
            ufs = Uf.query.filter_by(cod_regiao=int(regiao_id)).all()
        else:
            ufs = Uf.query.all()
        return jsonify([{"id": uf.id, "sigla": uf.sigla, "nome": uf.nome, "cod_regiao": uf.cod_regiao} for uf in ufs])
