from flask import request
from flask_restful import Resource
from helpers.database import db
from helpers.logging import logger
from models import Municipio  # Seu modelo SQLAlchemy para tb_mesorregiao

class MunicipiosResource(Resource):
    def get(self):
        logger.info("GET - Lista paginada de municipios")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("perPage", 50))
        offset = (page - 1) * per_page

        try:
            municipio = (
                db.session.query(Municipio)
                .order_by(Municipio.nome)
                .offset(offset)
                .limit(per_page)
                .all()
            )
            resultado = [
                {"id": e.id, "nome": e.nome, "cod_uf": e.co_uf, "cod_mesorregiao": e.co_mesorregiao, "cod_microrregiao": e.co_microrregiao} for e in municipio
            ]
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar municipios: %s", e)
            return {"mensagem": "Erro ao buscar municipios"}, 500

class MunicipioResource(Resource):
    def get(self, id):
        logger.info(f"GET - Mesorregião ID {id}")
        try:
            municipio = db.session.get(Municipio, id)
            if not municipio:
                return {"mensagem": "Mesorregião não encontrada"}, 404
            resultado = {"id": municipio.id, "nome": municipio.nome, "cod_uf": municipio.co_uf, "cod_mesorregiao": municipio.co_mesorregiao, "cod_microrregiao": municipio.co_microrregiao}
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar mesorregião: %s", e)
            return {"mensagem": "Erro ao buscar mesorregião"}, 500
