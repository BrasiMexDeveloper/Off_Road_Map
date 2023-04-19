from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_one(cls,data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_id(cls, data):
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;        
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) <1:
            return []
        return cls(results[0])  


    @classmethod
    def get_email(cls, data):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;        
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results)<1:
            return False
        return cls(results[0])    


    @staticmethod
    def validator(data):
        is_valid = True # we assume this is true

        if len(data['first_name']) < 1:
            is_valid = False
            flash("Must have a Name.")
        if len(data['last_name']) < 1:
            is_valid = False
            flash("Must have a last Name.")
        if len(data['email']) < 1:
            is_valid = False
            flash("Must have an  Email.")
        elif not EMAIL_REGEX.match(data['email']):
            flash("invalid email address")
            is_valid = False
        else:
            potential_email = {
                'email': data['email']
            }
            may_a_user = User.get_email(potential_email)
            if may_a_user:
                is_valid = False
                flash("email already exist!")

        if len(data['password']) < 1:
            is_valid = False
            flash("Password Required.")
        elif not data['password'] == data['confirm_password']:
            is_valid = False
            flash("password don't match")

        return is_valid    