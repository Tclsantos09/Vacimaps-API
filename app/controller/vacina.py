from app.models.table_vacina import Vacina
from app import db, app
from flask import request, jsonify
from app.controller.login import token_required

@app.route('/vacinas', methods=['GET'])
@token_required
def get_all_vacinas(current_user):
    dados = Vacina.query.filter_by().all()

    if not dados:
        return jsonify({'Mensagem': 'Nenhuma vacina cadastrada!'})

    vacinas = []

    for info in dados:
        vacina = {}
        vacina['id_vacina'] = info.id_vacina
        vacina['nome_vacina'] = info.nome_vacina
        vacina['num_duracao_meses'] = info.num_duracao_meses

        vacinas.append(vacina)

    return jsonify(vacinas)
