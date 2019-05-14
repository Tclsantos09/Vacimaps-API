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
import random

s = URLSafeTimedSerializer('this-is-secret') #melhorar essa chave de segurança


@app.route('/usuario', methods=['GET'])
@token_required
def get_one_user(current_user):
    user = Usuario.query.filter_by(id_usuario = current_user.id_usuario).first()
    vacinas_user = Usuario_Vacina.query.filter_by(id_usuario = current_user.id_usuario).all()

    if not user:
        return jsonify({'Mensagem': 'Usuário não encontrado!'})

    usuario = {}
    usuario['id_usuario'] = user.id_usuario
    usuario['nome'] = user.nome
    usuario['email'] = user.email
    usuario['validado'] = user.validado
    usuario['dt_nascimento'] = user.dt_nascimento

    vacinas = []
    if vacinas_user:        
        for vacina in vacinas_user:
            _vacina = {}
            nm_vacina = Vacina.query.filter_by(id_vacina = vacina.id_vacina).first()
            _vacina['vacina'] = nm_vacina.nome_vacina
            _vacina['reforço'] = nm_vacina.cd_reforco
            _vacina['id'] = vacina.id_usuario_vacina
            _vacina['id_vacina'] = vacina.id_vacina
            _vacina['data_vacina'] = vacina.data_vacina.strftime('%Y/%m/%d')
            _vacina['data_reforco'] = vacina.data_reforco.strftime('%Y/%m/%d')
            _vacina['local'] = vacina.ds_local_vacina
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

        if data['dt_nascimento']:
            usuario.dt_nascimento = data['dt_nascimento']

        db.session.commit()

        return jsonify({'Mensagem': 'Usuário alterado com sucesso!'})


#********************************* Enviar Email  ***********************
def send_code_confirm(email, texto, func):

    msg = Message('Confirm Email', sender='vacimaps@gmail.com', recipients=[email])
    usuario = Usuario.query.filter_by(email = email).first()

    i = 1
    while i < 2:
        code = str(random.randrange(100000, 999999))

        try:
            usuario.token_pswd_reset = code
            db.session.commit()
            break
        except exc.IntegrityError as e:
            db.session().rollback()

    msg.body = '{}{}'.format(texto, code)    
    mail.send(msg)

    return jsonify({'Mensagem': 'E-mail enviado com sucesso! Entre no seu E-mail para confirmar!'})

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

    return redirect('https://vacimaps-app-ionic.herokuapp.com/')


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    auth = request.get_json()

    usuario = Usuario.query.filter_by(email = auth['email']).first()

    if not usuario:
        return jsonify({'Mensagem': 'Usuario não encontrado!'})
    
    func = 'validar_token'
    texto = 'Olá, Tudo bem? \n\nPelo visto você esqueceu sua senha! Não tem problema, aqui está seu codigo para trocar a senha: '
    return send_code_confirm(usuario.email, texto, func)


@app.route('/validar_token', methods=['POST'])
def validar_token():
    data = request.get_json()
    
    usuario = Usuario.query.filter_by(token_pswd_reset = data['token']).first()

    if not usuario:
        return jsonify({'Mensagem': 'Código inválido!'})   

    return '{}'.format(usuario.id_usuario) 

@app.route('/reset_password', methods = ['PUT'])
def reset_password():
    data = request.get_json()
    usuario = Usuario.query.filter_by(id_usuario = data['id']).first()

    if not usuario:
        return jsonify({'Mensagem': 'Usuario não encontrado!'})
        
    data = request.get_json()

    if data['senha']:
        password = generate_password_hash(data['senha'])
        usuario.senha = password
        usuario.token_pswd_reset = None 

    db.session.commit()

    return jsonify({'Mensagem': 'Senha alterada com sucesso!'})

@app.route('/change_password', methods = ['PUT'])
@token_required
def change_password(current_user):
    data = request.get_json()
    usuario = Usuario.query.filter_by(id_usuario = current_user.id_usuario).first()

    if not usuario:
        return jsonify({'Mensagem': 'Usuario não encontrado!'})
        
    data = request.get_json()

    if check_password_hash(usuario.senha, data['senha_atual']):

        if data['nova_senha']:
            password = generate_password_hash(data['nova_senha'])
            usuario.senha = password
            usuario.token_pswd_reset = None 

        db.session.commit()

    else:
        return jsonify({'Mensagem': 'A senha atual errada!'})

    return jsonify({'Mensagem': 'Senha alterada com sucesso!'})

#***************************** VACINAS USUARIO ***************************

@app.route('/usuario/vacina/<id_vacina>', methods=['GET'])
@token_required
def get_one_user_vacina(current_user,id_vacina):
    vacinas_user = Usuario_Vacina.query.filter_by(id_usuario_vacina = id_vacina).first()    

    if not vacinas_user:
        return jsonify({'Mensagem': 'Vacina não encontrada!'})

    nm_vacina = Vacina.query.filter_by(id_vacina = vacinas_user.id_vacina).first()

    if vacinas_user:
        vacina = {}
        vacina['vacina'] = nm_vacina.nome_vacina
        vacina['reforço'] = nm_vacina.cd_reforco
        vacina['data_vacina'] = vacinas_user.data_vacina.strftime('%d/%m/%Y')
        vacina['data_reforco'] = vacinas_user.data_reforco.strftime('%d/%m/%Y')
        vacina['local'] = vacinas_user.ds_local_vacina

    else:
        return jsonify({'Mensagem': 'Nenhuma vacina encontrada!'})
    
    return jsonify(vacina)

@app.route('/usuario/vacina', methods=['POST'])
@token_required
def post_user_vacina(current_user):
    data = request.get_json()

    user_vacina = Usuario_Vacina(
        id_usuario = current_user.id_usuario,
        id_vacina=data['id_vacina'],
        ds_local_vacina=data['lote'], #Criar campo para o LOte no Banco e na Aplicação
        data_vacina=data['data_vacina'],
        data_reforco = '2020-03-06'
    )      

    try:
        db.session.add(user_vacina)
        db.session.commit()

    except exc.IntegrityError as e:

        return jsonify({'Mensagem': 'Erro ao cadastrar vacina!'})

    return jsonify({'Mensagem': "Vacina Cadastrada com sucesso'"})


@app.route('/usuario/vacina/<id_vacina>', methods=['PUT'])
@token_required
def edit_user_vacina(current_user,id_vacina):
    data = request.get_json()

    vacinas_user = Usuario_Vacina.query.filter_by(id_usuario_vacina = id_vacina).first()

    if not vacinas_user:
        return jsonify({'Mensagem': 'Vacina não encontrado!'})

    else:
        if data['id_vacina']:
            vacinas_user.id_vacina = data['id_vacina']
            
        if data['data_vacina']:
            vacinas_user.data_vacina = data['data_vacina']

        if data['ds_local_vacina']:
            vacinas_user.ds_local_vacina = data['ds_local_vacina']

        db.session.commit()

        return jsonify({'Mensagem': 'Vacina alterada com sucesso!'})


@app.route('/usuario/vacina/<id_vacina>', methods=['DELETE'])
@token_required
def del_user_vacina(current_user,id_vacina):

    vacinas_user = Usuario_Vacina.query.filter_by(id_usuario_vacina = id_vacina).first()

    if not vacinas_user:
        return jsonify({'Mensagem': 'Vacina não encontrado!'})

    else:
        db.session.delete(vacinas_user)
        db.session.commit()

        return jsonify({'Mensagem': 'Vacina deletada com sucesso!'})