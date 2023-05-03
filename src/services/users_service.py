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
        
    def insert_user(self, name: str, username: str, email: str, phone: str, hash_password: str, date_of_birth: datetime):
        try:
            sql =f"""
                INSERT INTO `users` (`name`, `username`, `email`, `phone`, `hash_password`, `date_of_birth`) 
                VALUES ('{name}', '{username}', '{email}', '{phone}', '{hash_password}', '{date_of_birth}');
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
                'date_of_birth': date_of_birth
            }, 'ok': True}, default=str)
        except Exception as e:
            return json.dumps({'erorr': str(e), 'ok': False}, default=str)
        finally:
            cur.close()
