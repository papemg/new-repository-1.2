# user.py
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_id, username, password,type):
        self.id = user_id
        self.username = username
        self.password_hash = self.hash_password(password)
        self.is_authenticated = False 
        self.type = type

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)
        
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False