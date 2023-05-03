import os 

CREDS = {}


CREDS['application_tokens'] = {
    os.environ['ADMIN_TOKEN']: "admin",
    }

CREDS['mysql'] = {} 
CREDS['mysql']['user'] = os.environ['DB_USER']
CREDS['mysql']['password'] = os.environ['DB_PASSWORD']
CREDS['mysql']['instance_connection_string'] = os.environ['DB_STRING']
CREDS['mysql']['charset'] = 'utf8mb4'
CREDS['mysql']['driver'] = 'pymysql'