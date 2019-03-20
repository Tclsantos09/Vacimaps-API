from app.models.table_usuario import Usuario
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
    info = Usuario.query.filter_by(id_usuario = current_user.id_usuario).first()

    if not info:
        return jsonify({'Mensagem': 'Usuário não encontrado!'})

    usuario = {}
    usuario['id_usuario'] = info.id_usuario
    usuario['nome'] = info.nome
    usuario['email'] = info.email
    usuario['validado'] = info.validado

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
        texto = 'Click ou Copie e Cole o link no seu navegador, para ser autenticado'

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

    msg.body = '{}: \n\n https://vacimaps-app.herokuapp.com{}'.format(texto,link)    
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
    if not auth or not auth['email']:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    usuario = Usuario.query.filter_by(email = auth['email']).first()

    if not usuario:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    func = 'validar_token'
    texto = 'Click ou Copie e Cole o link no seu navegador, para trocar sua senha'
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