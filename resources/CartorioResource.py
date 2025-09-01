# resources/CartorioResource.py
from flask_restful import Resource, reqparse
from flask import jsonify
from models import Cartorio
from helpers.database import db

# Parser para POST e PUT
cartorio_parser = reqparse.RequestParser()
cartorio_parser.add_argument("nome", type=str, required=True, help="Nome do cartório é obrigatório")
cartorio_parser.add_argument("email", type=str, required=False)
cartorio_parser.add_argument("cnpj", type=str, required=False)

class CartorioResource(Resource):
    # GET all
    def get(self):
        cartorios = Cartorio.query.all()
        return jsonify([
            {"id": c.id, "nome": c.nome, "email": c.email, "cnpj": c.cnpj} 
            for c in cartorios
        ])
    
    # POST
    def post(self):
        args = cartorio_parser.parse_args()
        novo_cartorio = Cartorio(
            nome=args["nome"],
            email=args.get("email"),
            cnpj=args.get("cnpj")
        )
        db.session.add(novo_cartorio)
        db.session.commit()
        return {"message": "Cartório criado com sucesso", "id": novo_cartorio.id}, 201

class CartorioDetailResource(Resource):
    # GET by id
    def get(self, id):
        cartorio = Cartorio.query.get(id)
        if cartorio:
            return jsonify({"id": cartorio.id, "nome": cartorio.nome, "email": cartorio.email, "cnpj": cartorio.cnpj})
        return {"message": "Cartório não encontrado"}, 404

    # PUT
    def put(self, id):
        cartorio = Cartorio.query.get(id)
        if not cartorio:
            return {"message": "Cartório não encontrado"}, 404
        
        args = cartorio_parser.parse_args()
        cartorio.nome = args["nome"]
        cartorio.email = args.get("email")
        cartorio.cnpj = args.get("cnpj")
        db.session.commit()
        return {"message": "Cartório atualizado com sucesso"}
    
    # DELETE
    def delete(self, id):
        cartorio = Cartorio.query.get(id)
        if not cartorio:
            return {"message": "Cartório não encontrado"}, 404
        
        db.session.delete(cartorio)
        db.session.commit()
        return {"message": "Cartório deletado com sucesso"}
