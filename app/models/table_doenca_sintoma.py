from app import db
from app.models.table_doenca import Doenca
from app.models.table_sintoma import Sintoma

class Doenca_Sintoma(db.Model):
    __tablename__:'doenca_sintoma'

    id_doenca_sintoma = db.Column(db.Integer,primary_key=True)    
    id_sintoma = db.Column(db.Integer, db.ForeignKey(Sintoma.id_sintoma))
    id_doenca = db.Column(db.Integer, db.ForeignKey(Doenca.id_doenca))

    def __init__(self, id_sintoma, id_doenca):
        self.id_sintoma = id_sintoma
        self.id_doenca = id_doenca