import pymysql 
from google.cloud.sql.connector import Connector
import json
from conf.passwords import CREDS
from datetime import datetime

class dbConnector():

    c = Connector()
    
    def __init__(self):
        self.cnx = self.c.connect(**CREDS['mysql'], database='microblog', cursorclass=pymysql.cursors.DictCursor)
    
    def __enter__(self):
        return self
    
    def get_all_users(self):
        try:
            cur = self.cnx.cursor()
            sql = """
                SELECT * FROM users;
            """
            cur.execute(sql)
            result = cur.fetchall()
            return json.dumps({'data': result, 'ok': True}, default=str)
        except Exception as e:
            return json.dumps({'erorr': e, 'ok': False}, default=str)
        
    def make_select(self, sql: str):
        try:
            cur = self.cnx.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            return json.dumps({'data': result, 'ok': True}, default=str)
        except Exception as e:
            return json.dumps({'erorr': e, 'ok': False}, default=str)
        finally:
            cur.close()
        
    def insert_user(self, name: str, username: str, email: str, phone: str, hash_password: str, date_of_birth: datetime, avatar: str):
        try:
            sql =f"""
                INSERT INTO `users` (`name`, `username`, `email`, `phone`, `hash_password`, `date_of_birth`, `avatar`) 
                VALUES ('{name}', '{username}', '{email}', '{phone}', '{hash_password}', '{date_of_birth}', '{avatar}');
            """ 
            cur = self.cnx.cursor()
            cur.execute(sql)
            self.cnx.commit()
            return json.dumps({'data': {
                'name': name, 
                'username': username, 
                'email': email,
                'phone': phone, 
                'password': hash_password, 
                'date_of_birth': date_of_birth,
                'avatar': avatar,
            }, 'ok': True}, default=str)
        except Exception as e:
            return json.dumps({'erorr in insert_user': str(e), 'ok': False}, default=str)
        finally:
            cur.close()

    def insert_post(self, user_id: int, content: str):
        try:
            sql =f"""
                INSERT INTO `posts` 
                (`user_id`, `content`) 
                VALUES 
                ('{user_id}', '{content}');
            """ 
            cur = self.cnx.cursor()
            cur.execute(sql)
            self.cnx.commit()
            return json.dumps({'data': {
                'user_id': user_id,
                'content': content
            }, 'ok': True}, default=str)
        except Exception as e:
            return json.dumps({'erorr': str(e), 'ok': False}, default=str)
        finally:
            cur.close()

    def delete_post(self, user_id: int, post_id: int):
        try:
            sql =f"""
                DELETE FROM `posts` WHERE (`post_id` = '{post_id}' AND `user_id` = '{user_id}');
            """ 
            cur = self.cnx.cursor()
            cur.execute(sql)
            self.cnx.commit()
            return json.dumps({'data': "Post apagado", 'ok': True}, default=str) if cur.rowcount > 0 else json.dumps({'data': "Nenhuma ação", 'ok': True}, default=str) 
        except Exception as e:
            return json.dumps({'erorr': str(e), 'ok': False}, default=str)
        finally:
            cur.close()
