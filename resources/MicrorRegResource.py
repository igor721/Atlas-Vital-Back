from flask import request
from flask_restful import Resource
from helpers.database import db
from helpers.logging import logger
from models import Microrregiao  # Seu modelo SQLAlchemy para tb_mesorregiao

class MicrorRegsResource(Resource):
    def get(self):
        logger.info("GET - Lista paginada de microrregioes")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("perPage", 50))
        offset = (page - 1) * per_page

        try:
            mecrorreg = (
                db.session.query(Microrregiao)
                .order_by(Microrregiao.nome)
                .offset(offset)
                .limit(per_page)
                .all()
            )
            resultado = [
                {"id": e.id, "nome": e.nome, "cod_uf": e.co_uf, "cod_mesorregiao": e.co_mesorregiao} for e in mecrorreg
            ]
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar microrregioes: %s", e)
            return {"mensagem": "Erro ao buscar microrregioes"}, 500

class MicrorRegResource(Resource):
    def get(self, id):
        logger.info(f"GET - Mesorregião ID {id}")
        try:
            mecrorreg = db.session.get(Microrregiao, id)
            if not mecrorreg:
                return {"mensagem": "Mesorregião não encontrada"}, 404
            resultado = {"id": mecrorreg.id, "nome": mecrorreg.nome, "cod_uf": mecrorreg.co_uf}
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar mesorregião: %s", e)
            return {"mensagem": "Erro ao buscar mesorregião"}, 500
