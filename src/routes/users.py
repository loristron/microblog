from flask import Blueprint, jsonify, make_response, request
from flasgger import swag_from
from flask_httpauth import HTTPTokenAuth
from conf.passwords import CREDS
from services.users_service import dbConnector
from werkzeug.security import generate_password_hash, check_password_hash
from tools.tools import is_valid_email, is_valid_date, convert_string_to_datetime
import json

token_auth = HTTPTokenAuth(scheme='Bearer')

database = dbConnector()

@token_auth.verify_token
def verify_token(token):
    if token in CREDS['application_tokens']:
        return CREDS['application_tokens'][token]

users = Blueprint('users', __name__, url_prefix='/api/users')

@users.route('/users',  methods=['GET'])
@token_auth.login_required
@swag_from('docs/get_users.yaml') 
def get_users():
    data = json.loads(database.get_all_users())
    return make_response(jsonify(data), 200)

@users.route('/create',  methods=['POST'])
@token_auth.login_required
@swag_from('docs/insert_user.yaml') 
def insert_user():
    try:
        name = request.form['name'].strip().replace("'", '`').title()
        username = request.form['username'].lower().strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip().replace('+55', '').replace(')', '').replace("(", '')
        date_of_birth = request.form['date_of_birth'].strip()
        password = request.form['password'].strip()

        ## Verificação de email 
        if not is_valid_email(email=email):
            return make_response(jsonify({'error': 'Enderço de email inválido'}))
        
        if not is_valid_date(date_string=date_of_birth):
            return make_response(jsonify({'error': 'Data de nascimento inválida'}))

        ## Verificação se usuário já existe 
        query_verifica = f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}'"
        verifica_db = json.loads(database.make_select(query_verifica))
        if verifica_db.get('ok'):
            if len(verifica_db.get('data')) > 0:
                return make_response(jsonify({'data': 'Email ou nome de usuário já cadastrados'}))
            
        date_of_birth = convert_string_to_datetime(date_string=date_of_birth)
        hashed_password = generate_password_hash(password)
        data = json.loads(database.insert_user(
            name=name, 
            username=username,
            email=email, 
            phone=phone,
            date_of_birth=date_of_birth,
            hash_password=hashed_password
            ))
        if data.get('ok'):
            return make_response(jsonify(data), 201)
        else:
            return make_response(jsonify({'error': 'Algo deu errado!'}), 400)
    except Exception as e:
        return make_response(jsonify({'error': str(e), 'ok': False}, 500))