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
    try:
        data = json.loads(database.get_all_users())
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)