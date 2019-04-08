from app import db
from app.models.table_usuario import Usuario
from app.models.table_vacina import Vacina

class Usuario_Vacina(db.Model):
    __tablename__:'usuario_vacina'

    id_usuario_vacina = db.Column(db.Integer,primary_key=True)    
    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id_usuario))
    id_vacina = db.Column(db.Integer, db.ForeignKey(Vacina.id_vacina))
    ds_local_vacina = db.Column(db.String(75))
    data_vacina = db.Column(db.Date())
    data_reforco = db.Column(db.Date())

    def __init__(self, id_usuario, id_vacina, ds_local_vacina, data_vacina,data_reforco):
        self.id_usuario = id_usuario
        self.id_vacina = id_vacina
        self.ds_local_vacina = ds_local_vacina
        self.data_vacina = data_vacina
        self.data_reforco = data_reforco