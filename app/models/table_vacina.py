from app import db

class Vacina(db.Model):
    __tablename__:'vacina'

    id_vacina = db.Column(db.Integer,primary_key=True)    
    nome_vacina = db.Column(db.String(45))
    cd_reforco = db.Column(db.Boolean)
    num_duracao_meses = db.Column(db.Integer)

    def __init__(self, nome_vacina, cd_reforco, num_duracao_meses):
        self.nome_vacina = nome_vacina
        self.cd_reforco = cd_reforco
        self.num_duracao_meses = num_duracao_meses
       