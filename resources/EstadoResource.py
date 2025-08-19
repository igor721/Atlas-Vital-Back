from flask_restful import Resource
from helpers.database import db
from helpers.logging import logger
from models import Uf  # Seu modelo SQLAlchemy para tb_uf

class EstadosResource(Resource):
    def get(self):
        logger.info("GET - Lista simples de estados")
        try:
            estados = db.session.query(Uf).order_by(Uf.nome).all()
            resultado = [
                {"id": e.id, "nome": e.nome, "sigla": e.sigla} for e in estados
            ]
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar estados: %s", e)
            return {"mensagem": "Erro ao buscar estados"}, 500

class EstadoResource(Resource):
    def get(self, id):
        logger.info(f"GET - Estado ID {id}")
        try:
            estado = db.session.get(Uf, id)
            if not estado:
                return {"mensagem": "Estado não encontrado"}, 404
            resultado = {"id": estado.id, "nome": estado.nome, "sigla": estado.sigla}
            return resultado, 200
        except Exception as e:
            logger.error("Erro ao buscar estado: %s", e)
            return {"mensagem": "Erro ao buscar estado"}, 500
