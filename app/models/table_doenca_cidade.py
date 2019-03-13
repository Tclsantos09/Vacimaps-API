from app import db
from app.models.table_doenca import Doenca
from app.models.table_cidade import Cidade

class Doenca_Cidade(db.Model):
    __tablename__:'doenca_cidade'

    id_doenca_cidade = db.Column(db.Integer,primary_key=True)    
    id_doenca = db.Column(db.Integer, db.ForeignKey(Doenca.id_doenca))
    id_cidade = db.Column(db.Integer, db.ForeignKey(Cidade.id_cidade))



    def __init__(self, id_doenca, id_cidade):
        self.id_doenca = id_doenca
        self.id_cidade = id_cidade