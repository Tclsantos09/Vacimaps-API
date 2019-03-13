from app import db
from app.models.table_vacina import Vacina
from app.models.table_doenca import Doenca

class Vacina_Doenca(db.Model):
    __tablename__:'vacina_doenca'

    id_vacina_doenca = db.Column(db.Integer,primary_key=True)    
    id_vacina = db.Column(db.Integer, db.ForeignKey(Vacina.id_vacina))
    id_doenca = db.Column(db.Integer, db.ForeignKey(Doenca.id_doenca))


    def __init__(self, id_vacina, id_doenca):
        self.id_vacina = id_vacina
        self.id_doenca = id_doenca