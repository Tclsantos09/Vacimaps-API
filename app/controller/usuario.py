from app.models.table_usuario import Usuario
from app import db, app
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.controller.login import token_required


@app.route('/usuario/<user_id>', methods=['GET'])
@token_required
def get_one_user(current_user, user_id):
    info = Usuario.query.filter_by(id_usuario = user_id).first()

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

    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify({'Mensagem': 'O email informado já está cadastrado!'})

    return jsonify({'Mensagem': 'Usuário adicionado com sucesso!'})

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
