#!/usr/bin/env python

class ResourceManager():

    def __init__(self, db):
        self.db = db

    def create(self, user_id, name, path, body):
        """Create a new resource owned by the provided user"""

        if self.db.get_resource(user_id, path) is not None:
            # Resource exists already
            # TODO throw an exception
            return None

        return self.db.create_resource(user_id, name, path, body)

    def get_resource_description(self, user_name, path):
        resource = self.db.get_resource_by_user_name(user_name, path)

        if resource is None:
            return {}

        del resource['_id']

        return resource

    def get_resource_body(self, user_name, path):
        resource = self.get_resource_description(user_name, path)

        return resource['body']