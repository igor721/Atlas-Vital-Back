from flask import request
from flask_restful import Resource
from helpers.database import db
from helpers.logging import logger
from models import Mesorregiao  # Seu modelo SQLAlchemy para tb_mesorregiao

class MesorRegsResource(Resource):
    def get(self):
        logger.info("GET - Lista paginada de mesorregiões")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("perPage", 50))
        offset = (page - 1) * per_page

        try:
            mesorreg = (
                db.session.query(Mesorregiao)
                .order_by(Mesorregiao.nome)
                .offset(offset)
                .limit(per_page)
                .all()
            )
            resultado = [
                {"id": e.id, "nome": e.nome, "cod_uf": e.co_uf} for e in mesorreg
            ]
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar mesorregiões: %s", e)
            return {"mensagem": "Erro ao buscar mesorregiões"}, 500

class MesoRegResource(Resource):
    def get(self, id):
        logger.info(f"GET - Mesorregião ID {id}")
        try:
            mesorreg = db.session.get(Mesorregiao, id)
            if not mesorreg:
                return {"mensagem": "Mesorregião não encontrada"}, 404
            resultado = {"id": mesorreg.id, "nome": mesorreg.nome, "cod_uf": mesorreg.co_uf}
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar mesorregião: %s", e)
            return {"mensagem": "Erro ao buscar mesorregião"}, 500
