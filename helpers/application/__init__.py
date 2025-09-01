from flask import Flask
from flask_restful import Api

app = Flask(__name__) #inicializo
api = Api(app) #preparo para recerber rotas 
