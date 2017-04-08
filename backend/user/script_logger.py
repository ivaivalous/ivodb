#!/usr/bin/env python

MAX_LOG_LENGTH = 1000

def save(db, user_name, path, logs):
    # Don't save empty logs
    if len(logs) == 0:
        return

    # If logs are longer than the maximum
    # allowed, trim them to the last MAX_LOG_LENGTH
    # messages.
    if len(logs) > MAX_LOG_LENGTH:
        logs = logs[-MAX_LOG_LENGTH:]


    user_id = db.get_user_id(user_name)
    if user_id is None:
        return

    return db.save_logs(user_id, path, logs)
