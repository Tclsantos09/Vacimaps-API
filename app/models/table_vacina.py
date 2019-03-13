from app import db

class Vacina(db.Model):
    __tablename__:'vacina'

    id_vacina = db.Column(db.Integer,primary_key=True)    
    nome_vacina = db.Column(db.String(45))
    ds_vacina = db.Column(db.String(75))

    def __init__(self, nome_vacina, ds_vacina):
        self.nome_vacina = nome_vacina
        self.ds_vacina = ds_vacina
       