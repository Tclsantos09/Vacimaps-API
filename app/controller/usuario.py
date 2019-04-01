from app.models.table_usuario import Usuario
from app.models.table_usuario_vacina import Usuario_Vacina
from app.models.table_vacina import Vacina
from app import db, app, mail
from flask import request, jsonify,url_for, make_response, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from app.controller.login import token_required
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from sqlalchemy import exc
from flask_mail import Message

s = URLSafeTimedSerializer('this-is-secret') #melhorar essa chave de segurança


@app.route('/usuario', methods=['GET'])
@token_required
def get_one_user(current_user):
    user = Usuario.query.filter_by(id_usuario = current_user.id_usuario).first()
    vacinas_user = Usuario_Vacina.query.filter_by(id_usuario_vacina = current_user.id_usuario).first()

    if not user:
        return jsonify({'Mensagem': 'Usuário não encontrado!'})

    usuario = {}
    usuario['id_usuario'] = user.id_usuario
    usuario['nome'] = user.nome
    usuario['email'] = user.email
    usuario['validado'] = user.validado

    vacinas = []
    if vacinas_user:
        _vacina = {}
        for vacina in vacinas_user:
            nm_vacina = Vacimaps.query.filter_by(id_vacina = vacina.id_vacina).firt()
            _vacina['vacina'] = nm_vacina.nome_vacina
            #_vacina['Data'] = vacina.data_vacina
            _vacina['descricao'] = nm_vacina.ds_vacina
        vacinas.append(_vacina)
        usuario['vacinas'] = vacinas
    else:
        usuario['vacinas'] = "Nenhuma vacina cadastrada!"
    
    return jsonify(usuario)


@app.route('/usuario', methods=['POST'])
def post_user():
    data = request.get_json()
    password = generate_password_hash(data['senha'])

    usuario = Usuario(
        nome = data['nome'],
        email=data['email'],
        senha=password,
        validado=False
    )    

    try:
        db.session.add(usuario)
        db.session.commit()

        func = 'email_confirm'
        texto = 'Olá, Tudo bem? \n\n Seja bem vindo ao Vacimaps, click no link abaixo, para ser autenticado!'

    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify({'Mensagem': 'O email informado já está cadastrado!'})

    return send_email_confirm(usuario.email, texto, func)

    #return jsonify({'Mensagem': 'Usuário adicionado com sucesso!'})

@app.route('/usuario', methods=['PUT'])
@token_required
def edit_usuario(current_user):
    usuario = Usuario.query.filter_by(id_usuario = current_user.id_usuario).first()

    if not usuario:
        return jsonify({'Mensagem': 'Usuário não encontrado!'})

    else:
        data = request.get_json()

        if data['nome']:
            usuario.nome = data['nome']

        if data['email']:
            usuario.email = data['email']

        db.session.commit()

        return jsonify({'Mensagem': 'Usuário alterado com sucesso!'})


#********************************* Enviar Email  ***********************
def send_email_confirm(email, texto, func):
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='vacimaps@gmail.com', recipients=[email])

    link = url_for('.{}'.format(func), token = token, external = True)

    msg.body = '{}\nhttps://vacimaps-app.herokuapp.com{}'.format(texto,link)    
    mail.send(msg)

    return jsonify({'Mensagem': 'E-mail enviado com sucesso! Entre no seu E-mail para confirmar!'})

@app.route('/emailconfirm/<token>')
def email_confirm(token):
    try:
        email = s.loads(token, salt='email-confirm')

        usuario = Usuario.query.filter_by(email = email).first()

        if not usuario:
            return jsonify({'Mensagem': 'Usuário não encontrado'})
        
        usuario.validado = True
        db.session.commit()

    except SignatureExpired:        
        return "link expirado!"

    return jsonify({'Mensagem': "E-mail verificado com sucesso!"})


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    auth = request.get_json()

    usuario = Usuario.query.filter_by(email = auth['email']).first()

    if not usuario:
        return jsonify({'Mensagem': 'Usuario não encontrado!'})
    
    func = 'validar_token'
    texto = 'Olá, Tudo bem? \n\nPelo visto você esqueceu sua senha! Não tem problema, click no link abaixo para troca-la!'
    return send_email_confirm(usuario.email, texto, func)


@app.route('/validar_token/<token>')
def validar_token(token):
    try:
        email = s.loads(token, salt='email-confirm')

        usuario = Usuario.query.filter_by(email = email).first()

        if not usuario:
            return jsonify({'Mensagem': 'Usuário não encontrado'})        
        
    except SignatureExpired:        
        return "link expirado!"

    return 'Tela de redirecionamento/id do usuario = {}'.format(usuario.id_usuario)

@app.route('/reset_password/<id>', methods = ['PUT'])
def reset_password(id):
    usuario = Usuario.query.filter_by(id_usuario = id).first()

    if not usuario:
        return jsonify({'Mensagem': 'Usuário não encontrado'})
        
    data = request.get_json()

    if data['senha']:
        password = generate_password_hash(data['senha'])
        usuario.senha = password

    db.session.commit()

    return jsonify({'Mensagem': 'Senha alterado com sucesso!'})