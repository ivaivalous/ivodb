#!/usr/bin/env python

import config_reader

from pymongo import MongoClient
from bson.objectid import ObjectId


class Database:

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

    def get_user_id(self, user_name):
        user = self.get_user(user_name=user_name)

        if user is None:
            return None

        return str(user['_id'])

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

    def update_user(self, user_id, user_name, email, display_name, password_hash):
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
        user_id = self.get_user_id(username)
        if user_id is None:
            return None

        return self.get_resource(user_id, path)

    def create_resource(
            self, user_id, name, path, res_type, body, headers, published):

        return self.db.resources.insert_one({
            "userId": user_id,
            "name": name,
            "path": path,
            "type": res_type,
            "body": body,
            "headers": headers,
            "published": published
        }).inserted_id

    def update_resource(
            self, user_id, name, path, new_path, res_type, body, headers, published):

        return self.db.resources.update_one(
            {"$and": [
                {"userId": user_id},
                {"path": path}
            ]},
            {"$set": {
                "name": name,
                "path": new_path,
                "type": res_type,
                "body": body,
                "headers": headers,
                "published": published
            }
            }
        )

    def set_resource_public(self, user_id, path, published):
        return self.db.resources.update_one(
            {"$and": [
                {"userId": user_id},
                {"path": path}
            ]},
            {"$set": {
                "published": published
            }
            }
        )

    # Delete a resource. resource_id would normally be sufficient,
    # user_id is used to help with delete permission validation
    def delete_resource(self, user_id, resource_id):
        return self.db.resources.delete_one({
            "userId": user_id,
            "_id": ObjectId(resource_id)
        })

    # Save logs belonging to a given user for a given script
    def save_logs(self, user_id, path, logs):
        return self.db.logs.insert_one({
            "userId": user_id,
            "path": path,
            "logs": logs
        }).inserted_id

    # Get all logs for a specific user, on a specific script
    def get_logs(self, user_id, path):
        return self.db.logs.find({
            "$and": [
                {"userId": user_id},
                {"path": path}
            ]
        })
