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

def load(db, user_name, path):
    all_messages = []
    user_id = db.get_user_id(user_name)
    if user_id is None:
        return None

    log_records = db.get_logs(user_id, path)
    for entry in log_records:
        all_messages.append(transform_message(entry))

    return str(all_messages)

def transform_message(log_entry):
    result = []
    logs = log_entry["logs"]

    for entry in logs:
        result.append({
            "time": entry["time"],
            "message": entry["message"]
        })

    return result

