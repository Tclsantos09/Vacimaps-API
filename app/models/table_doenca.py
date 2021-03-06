from app import db

class Doenca(db.Model):
    __tablename__:'doenca'

    id_doenca = db.Column(db.Integer,primary_key=True)    
    nome_doenca = db.Column(db.String(100))
    ds_doenca = db.Column(db.String(500))
    recomendacao = db.Column(db.String(1000))

    def __init__(self, nome_doenca, ds_doenca, recomendacao):
        self.nome_doenca = nome_doenca
        self.ds_doenca = ds_doenca