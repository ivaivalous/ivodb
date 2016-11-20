#!/usr/bin/env python

import config_reader
import bcrypt
import jwt


class Password():

    @staticmethod
    def generate_salt():
        return bcrypt.gensalt()

    @staticmethod
    def get_password_hash(password, salt):
        """Create a hashed password"""
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def check_password(password, password_hash):
        """Check if the provided password matches the hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'), password_hash.encode('utf-8'))


class Jwt():
    """Responsible for creation and validation of JWT tokens"""

    def __init__(self):
        self.algorithm = config_reader.config['jwtSettings']['algorithm']
        self.secret = config_reader.config['jwtSettings']['secret']

    def generate_jwt(self, data):
        return jwt.encode(data, self.secret, algorithm=self.algorithm)

    def validate_jwt(self, token):
        try:
            payload = jwt.decode(
                token, self.secret, algorithms=[self.algorithm])
            return True
        except jwt.InvalidTokenError:
            return False