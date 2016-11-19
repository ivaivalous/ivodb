#!/usr/bin/env python

import config_reader
import pymongo
from pymongo import MongoClient

class Database():

    def __init__(self):
        self.db_config = config_reader.config['databaseSettings']
        self.client = MongoClient(
            self.db_config['host'], self.db_config['port'])

        self.db = self.client.ivodb

    def user_exists(self, user_name=None, email=None):
        """Check if a user exists by username or email"""
        if user_name is None and email is None:
            return False

        user = self.db.users.find_one({
            "$or": [
                {"username": user_name},
                {"email": email}
            ]
        })

        return user is not None

    def get_user(self, user_name=None, email=None):
        """Get a user from the database"""
        if user_name is None and email is None:
            return None

        user = self.db.users.find_one({
            "$or": [
                {"username": user_name},
                {"email": email}
            ]
        })

        return user

    def create_user(self, user_name, email, password_hash, display_name=""):
        """Create a new user"""
        if self.user_exists(user_name, email):
            """User names and emails must be unique"""
            raise ValueError("User already exists")

        return self.db.users.insert_one({
            "username": user_name,
            "email": email,
            "hash": password_hash,
            "displayName": display_name,
            "active": True
        }).inserted_id

    def update_user(self, id, user_name, email, display_name, password_hash):
        pass