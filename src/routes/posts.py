from flask import Blueprint, jsonify, make_response, request
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
    
@posts.route('/create',  methods=['POST'])
@token_auth.login_required
@swag_from('docs/create_post.yaml') 
def create_post():
    try:
        user_id = request.form['user_id']
        content = request.form['content'].replace("'", '`')

        if len(content) > 240:
            return make_response(jsonify({'data': 'Limite de caracteres excedido'}), 400)

        validate = json.loads(database.make_select(sql=f"SELECT user_id FROM users WHERE user_id = '{user_id}'"))
        if not validate.get('ok') or len(validate.get('data')) == 0:
            return make_response(jsonify({'data': 'Usuário não encontrado'}), 404)
        
        insert_post = json.loads(database.insert_post(user_id=user_id, content=content))
        if insert_post.get('ok'):
            return make_response(jsonify({'data': insert_post}), 201)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    
@posts.route('/delete',  methods=['POST'])
@token_auth.login_required
@swag_from('docs/delete_post.yaml') 
def delete_post():
    try:
        user_id = request.form['user_id']
        post_id = request.form['post_id']
        delete = json.loads(database.delete_post(user_id=user_id, post_id=post_id))
        return make_response(jsonify({'data': delete}))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    
