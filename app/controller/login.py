from app import app, db
from app.models.table_usuario import Usuario
from flask import request, jsonify, make_response, redirect, url_for, session
from werkzeug.security import check_password_hash
from werkzeug.wrappers import Response
from werkzeug.datastructures import Headers
import jwt
import datetime
from functools import wraps


def token_required(f):
    @wraps(f)
    def decoreted(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']
        
        if not token:
            return jsonify({'Mensagem': 'Você precisa de uma Token para ter acesso!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Usuario.query.filter_by(id_usuario = data['id_usuario']).first()
        except:
            return jsonify({'Mensagem': 'Token invalida!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decoreted


@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth['email'] or not auth['password']:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    usuario = Usuario.query.filter_by(email = auth['email']).first()

    if not usuario:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if check_password_hash(usuario.senha, auth['password']):
        token = jwt.encode({'id_usuario': usuario.id_usuario, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        
        return jsonify({'token': token.decode('UTF-8')})
    
    return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route('/')
def index():
    return "<h1> API do Back </h1><p>Para testar basta usuar o Postman e seguir as intruções do README.MD, disponivel no <a href='https://github.com/Tclsantos09/Vacimaps-API'>GitHUB</a></p>"