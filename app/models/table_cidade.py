from app import db

class Cidade(db.Model):
    __tablename__:'cidade'

    id_cidade = db.Column(db.Integer,primary_key=True)    
    nome_cidade = db.Column(db.String(45))
    uf_cidade = db.Column(db.String(45))

    def __init__(self, nome_cidade, uf_cidade):
        self.nome_cidade = nome_cidade
        self.uf_cidade = uf_cidade
       