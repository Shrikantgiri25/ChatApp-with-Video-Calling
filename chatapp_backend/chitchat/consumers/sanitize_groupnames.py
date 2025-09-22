import re


def sanitize_group_name(name):
    # Replace invalid characters with underscore
    return re.sub(r"[^a-zA-Z0-9_\-\.]", "_", name)[:100]


def sanitize_notification_group_name(name):
    return re.sub(r"[^a-zA-Z0-9._-]", "_", str(name))[:99]
