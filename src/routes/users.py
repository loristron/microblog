from flask import Blueprint, jsonify, make_response
from flasgger import swag_from
from flask_httpauth import HTTPTokenAuth
from conf.passwords import CREDS
from services.users_service import dbConnector
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
    try:
        data = json.loads(database.get_all_users())
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)