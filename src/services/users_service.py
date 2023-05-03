import pymysql 
from google.cloud.sql.connector import Connector
import json
from conf.passwords import CREDS

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