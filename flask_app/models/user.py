from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB_NAME
from flask import flash
import re
from flask_bcrypt import Bcrypt, check_password_hash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes_made = [] # From our own logic

    #! CREATE
    @classmethod
    def save(cls, form_data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL(DB_NAME).query_db(query, form_data)
        return user_id
    
    # Find a user by email
    @classmethod
    def get_by_email(cls, email):
        email_dict = {'email' : email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB_NAME).query_db(query, email_dict)
        if len(result) < 1:
            return False
        found_user = cls(result[0])
        return found_user
            

    @staticmethod
    def validate_user(data):
        is_valid = True
        #  Check the length of first_name
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters", "register")
            is_valid = False

            #  Check the length of last_name
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters", "register")
            is_valid = False

            #  Check the length of password
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False

            #  Check password and comfirm are same
        if data['password'] != data['confirm_pw']:
            flash("Password and Confirm password must match", "register")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email", "register")
            is_valid = False

        # Check email exist
        if User.get_by_email(data['email']):
            flash("Email already registered", "register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        is_valid = True

        potential_user = User.get_by_email(form_data['email'])

        if not potential_user:
            flash("Invalid Email/Password", "login")
            is_valid = False
        else:
            if not check_password_hash(potential_user.password, form_data['password']):
                flash("Invalid Email/Password", "login")
                is_valid = False
        return is_valid
    
    #! READ ONE
    @classmethod
    def get_one_by_id(cls, id):
        id_dict = {'id':id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB_NAME).query_db(query, id_dict)
        user = cls(result[0])
        return user
