#!/usr/bin/env python
import json


class ResourceManager:

    def __init__(self, db):
        self.db = db

    def create(self, user_id, name, path, type, body, headers):
        """Create a new resource owned by the provided user"""

        if self.db.get_resource(user_id, path) is not None:
            # Resource exists already
            # Overwrite the resource
            return self.db.update_resource(
                user_id, name, path, path, type, body, headers, True)

        return self.db.create_resource(
            user_id, name, path, type, body, headers, True)

    def get_resource(self, user_name, path):
        resource = self.db.get_resource_by_user_name(user_name, path)

        if resource is None:
            return resource

        del resource['_id']

        return resource

    def get_resources(self, user_id):
        return self.db.get_resources(user_id)

    def get_resource_for_display(self, user_name, path):
        resource = self.get_resource(user_name, path)

        if resource is None or resource['published'] is not True:
            return None, {}, "text"

        try:
            headers = json.loads(resource['headers'])
        except:
            # Headers have not been specified or were of invalid format
            headers = {}

        return resource['body'], headers, resource['type']

    def activate(self, user_id, path):
        self.db.set_resource_public(user_id, path, True)

    def deactivate(self, user_id, path):
        self.db.set_resource_public(user_id, path, False)

    def delete(self, user_id, resource_id):
        self.db.delete_resource(user_id, resource_id)