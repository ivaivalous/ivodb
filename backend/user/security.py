#!/usr/bin/env python

import bcrypt


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

    @staticmethod
    def generate_jwt(data):
        pass

    @staticmethod
    def validate_jwt(jwt):
        pass