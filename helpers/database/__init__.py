from flask_sqlalchemy import SQLAlchemy
from helpers.application import app
from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/AtlasVital' #Configuração

db = SQLAlchemy(app) #iniciando sqlAlchemy
migrate = Migrate(app, db) #uniciando migrate com app e db