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

posts = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts.route('/posts',  methods=['GET'])
@token_auth.login_required
@swag_from('docs/get_all_posts.yaml') 
def get_posts():
    try:
        data = json.loads(database.make_select("""SELECT * FROM posts;"""))
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    
