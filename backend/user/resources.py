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

        return self.db.create_resource(user_id, name, path, body, True)

    def get_resource(self, user_name, path):
        resource = self.db.get_resource_by_user_name(user_name, path)

        if resource is None:
            return {}

        del resource['_id']

        return resource

    def get_resources(self, user_id):
        return self.db.get_resources(user_id)

    def get_resource_body(self, user_name, path):
        resource = self.get_resource(user_name, path)

        if 'body' not in resource or resource['published'] is not True:
            return None

        return resource['body']