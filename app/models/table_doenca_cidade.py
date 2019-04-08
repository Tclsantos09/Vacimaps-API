from app import db
from app.models.table_doenca import Doenca
from app.models.table_cidade import Cidade
from app.models.table_vacina import Vacina

class Doenca_Cidade(db.Model):
    __tablename__:'doenca_cidade'

    id_doenca_cidade = db.Column(db.Integer,primary_key=True)    
    id_doenca = db.Column(db.Integer, db.ForeignKey(Doenca.id_doenca))
    id_vacina = db.Column(db.Integer, db.ForeignKey(Vacina.id_vacina))
    id_cidade = db.Column(db.Integer, db.ForeignKey(Cidade.id_cidade))
    cd_nivel_alerta = db.Column(db.Integer)
    ds_descricao = db.Column(db.String(200))



    def __init__(self, id_doenca, id_vacina, id_cidade, cd_nivel_alerta, ds_descricao):
        self.id_doenca = id_doenca
        self.id_vacina = id_vacina
        self.id_cidade = id_cidade
        self.cd_nivel_alerta = cd_nivel_alerta
        self.ds_descricao = ds_descricao