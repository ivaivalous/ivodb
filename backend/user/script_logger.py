#!/usr/bin/env python

MAX_LOG_LENGTH = 1000
MESSAGE_MAX_LENGTH = 2000

class ScriptLogger():

    def __init__(self, db):
        self.db = db

    def save(self, user_name, path, logs):
        # Don't save empty logs
        if len(logs) == 0:
            return

        # If logs are longer than the maximum allowed,
        # trim them to the last MAX_LOG_LENGTH messages.
        if len(logs) > MAX_LOG_LENGTH:
            logs = logs[-MAX_LOG_LENGTH:]

        all_messages = self.transform_log_entries(logs)

        user_id = self.db.get_user_id(user_name)
        if user_id is None:
            return

        return self.db.save_logs(user_id, path, all_messages)

    def load(self, user_name, path):
        all_messages = []
        user_id = self.db.get_user_id(user_name)
        if user_id is None:
            return None

        log_records = self.db.get_logs(user_id, path)
        for entry in log_records:
            all_messages.append(self.transform_messages(entry))

        return str(all_messages)

    def transform_messages(self, log_entry):
        result = []
        logs = log_entry["logs"]

        for entry in logs:
            result.append(self.transform_log_entries([entry]))

        return result

    def transform_log_entries(self, log):
        result = []

        for entry in log:
            try:
                message = str(entry["message"])
                time = int(entry["time"])
            except Exception as e:
                # Messages were of incorrect format,
                # ignore them and return empty
                print(e)
                return result

            result.append({
                "time": time,
                "message": message
            })

        return result




