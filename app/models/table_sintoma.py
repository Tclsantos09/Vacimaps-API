from app import db

class Sintoma(db.Model):
    __tablename__:'sintoma'

    id_sintoma = db.Column(db.Integer,primary_key=True)    
    nome_sintoma= db.Column(db.String(50))

    def __init__(self, nome_sintoma):
        self.nome_sintoma = nome_sintoma