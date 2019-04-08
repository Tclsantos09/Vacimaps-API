from app import db

class Usuario(db.Model):
    __tablename__:'usuario'

    id_usuario = db.Column(db.Integer,primary_key=True)    
    nome = db.Column(db.String(75))
    email = db.Column(db.String(45), unique = True)
    senha = db.Column(db.String(500))
    validado = db.Column(db.Boolean)
    token_pswd_reset = db.Column(db.Integer, unique = True)
    dt_nascimento = db.Column(db.Date)

    def __init__(self, nome, email, senha, validado):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.validado = validado
       