import re
from datetime import datetime

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def is_valid_date(date_string):
    try:
        # Tenta criar um objeto datetime a partir da string de data fornecida
        date_obj = datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        # Se a criação do objeto datetime falhar, a data é inválida
        return False
    
def convert_string_to_datetime(date_string):
    data_nascimento = datetime.strptime(date_string, '%d/%m/%Y').date()
    return data_nascimento
