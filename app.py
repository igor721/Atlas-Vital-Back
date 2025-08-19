from helpers.database import app, db
from helpers.CORS import cors

from helpers.application import api
from models import Regiao, Uf, UfEstatistica, Mesorregiao, Microrregiao, Municipio, MunicipioEstatistica

from resources.EstadoResource import EstadosResource, EstadoResource
from resources.MesorRegResource import MesorRegsResource, MesoRegResource
from resources.MicrorRegResource import MicrorRegsResource, MicrorRegResource
from resources.MunicipioResource import MunicipiosResource, MunicipioResource

from resources.IndexResource import IndexResource


cors.init_app(app)

api.add_resource(IndexResource, '/')

# EndPoint Estados
api.add_resource(EstadosResource, '/estados')
api.add_resource(EstadoResource, '/estados/<int:id>')

# endPoint Mesor
api.add_resource(MesorRegsResource, '/mesoregioes')
api.add_resource(MesoRegResource, '/mesoregioes/<int:id>')

# endPoint Micro
api.add_resource(MicrorRegsResource, '/microregioes')
api.add_resource(MicrorRegResource, '/microregioes/<int:id>')

# endPoint Municipio
api.add_resource(MunicipiosResource, '/municipios')
api.add_resource(MunicipioResource, '/municipios/<int:id>')



