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


    def get_resource(self, user_id, path):
        if user_id is None or path is None:
            return None

        return self.db.resources.find_one({
            "$and": [
                {"userId": user_id},
                {"path": path}
            ]
        })

    def get_resources(self, user_id):
        return self.db.resources.find({
            "userId": user_id
        })

    def get_resource_by_user_name(self, username, path):
        user = self.get_user(user_name=username)

        if user is None:
            return None

        user_id = str(user['_id'])

        return self.get_resource(user_id, path)

    def create_resource(self, user_id, name, path, body, published):
        return self.db.resources.insert_one({
            "userId": user_id,
            "name": name,
            "path": path,
            "type": "text",
            "body": body,
            "published": published
        }).inserted_id