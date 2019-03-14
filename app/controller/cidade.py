from app.models.table_cidade import Cidade
from app import db, app
from flask import request, jsonify
from app.controller.login import token_required

@app.route('/cidades', methods=['GET'])
@token_required
def get_all_city(current_user):
    dados = Cidade.query.filter_by().all()

    if not dados:
        return jsonify({'Mensagem': 'Nenhuma cidade cadastrada!'})

    cidades = []

    for info in dados:
        cidade = {}
        cidade['id_cidade'] = info.id_cidade
        cidade['nome_cidade'] = info.nome_cidade
        cidade['uf_cidade'] = info.uf_cidade

        cidades.append(cidade)

    return jsonify(cidades)


@app.route('/cidades/<cidade_id>', methods=['GET'])
@token_required
def get_one_city(current_user, cidade_id):
    info = Cidade.query.filter_by(id_cidade = cidade_id).first()

    if not info:
        return jsonify({'Mensagem': 'Cidade não encontrado!'})

    cidade = {}
    cidade['id_cidade'] = info.id_cidade
    cidade['nome_cidade'] = info.nome_cidade
    cidade['uf_cidade'] = info.uf_cidade

    return jsonify(usuario)
