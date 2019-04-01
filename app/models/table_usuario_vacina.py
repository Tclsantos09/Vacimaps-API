from app import db
from app.models.table_usuario import Usuario
from app.models.table_vacina import Vacina

class Usuario_Vacina(db.Model):
    __tablename__:'usuario_vacina'

    id_usuario_vacina = db.Column(db.Integer,primary_key=True)    
    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id_usuario))
    id_vacina = db.Column(db.Integer, db.ForeignKey(Vacina.id_vacina))
    data_vacina = db.Column(db.Date())

    def __init__(self, nome_doenca, id_vacina, data_vacina):
        self.id_usuario = id_usuario
        self.id_vacina = id_vacina
        self.data_vacina = data_vacina