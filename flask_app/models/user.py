from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_register(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("User first name must be at least 2 characters")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("User last name must be at least 2 characters")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("User password must be at least 8 characters")
            is_valid = False
        if not form_data['password'] == form_data['conf_pass']:
            flash("Password and Confirmation Password must match!")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Email must be a valid format!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(validation_data):
        is_valid = True
        if not validation_data ['user']:
            flash("Invalid Email/Password")
            is_valid = False
        elif not bcrypt.check_password_hash(validation_data ['user'].password, validation_data['password']):
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid

    @classmethod
    def register_user( cls, data ):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"

        results = connectToMySQL('babyjoy').query_db( query, data )
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("babyjoy").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_info( cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"

        results = connectToMySQL('babyjoy').query_db( query, data )

        return cls(results[0])