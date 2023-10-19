from fake_pinterest import database
from datetime import datetime

class Usuario(database.Model):
    id = database.Collumn(database.Integer, primary_key=True)
    username = database.Collumn(database.String, nullable=False, unique=True)
    email = database.Collumn(database.String, nullable=False, unique=True)
    senha = database.Collumn(database.String, nullable=False)
    fotos = database.relationship()


class Foto(database.Model):
    id = database.Collumn(database.Integer, primary_key=True)
    imagem = database.Collumn(database.String, default="default.png")
    data_criacao = database.Collumn(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Collumn()