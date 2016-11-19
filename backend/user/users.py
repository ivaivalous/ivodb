#!/usr/bin/env python

from security import Password

class UserManager():

    def __init__(self, db):
        self.db = db

    def login(self, username, password):
        """Log in"""
        user = self.db.get_user(username, username)

        if user is None:
            return None

        if Password.check_password(password, user['hash']):
            return user
        return None

    def register(self, username, email, password, display_name=""):
        """Register"""
        salt = Password.generate_salt()
        password_hash = Password.get_password_hash(password, salt)

        return self.db.create_user(
            username, email, password_hash, display_name)

    def reset_password(self, username, email):
        """Reset forgotten password"""
        pass
