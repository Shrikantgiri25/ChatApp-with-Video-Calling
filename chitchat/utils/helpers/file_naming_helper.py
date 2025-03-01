import os, uuid


def create_unique_filename(instance, filename):
    file_extension = filename.split(".")[-1]
    if hasattr(instance, "user"):
        name = instance.user.username
        folder_name = "profile_pictures"
    elif hasattr(instance, "group_name"):
        name = instance.group_name.replace(" ", "_")
        folder_name = "group_avatars"
    elif hasattr(instance, "content_type"):
        if hasattr(instance.content_type.startswith("image")):
            name = instance.uploaded_by.username
            folder_name = "message_attachments/images"
        elif hasattr(instance.content_type.startswith("video")):
            name = instance.uploaded_by.username
            folder_name = "message_attachments/videos"
        elif hasattr(instance.content_type.startswith("audios")):
            name = instance.uploaded_by.username
            folder_name = "message_attachments/audios"
        elif hasattr(instance.content_type.startswith("documents")):
            name = instance.uploaded_by.username
            folder_name = "message_attachments/documents"
        else:
            name = instance.uploaded_by.username
            folder_name = "message_attachments/others"
    else:
        name = "unknown"
        folder_name = "uploads"

    file_name = f"{name}_{uuid.uuid4().hex}.{file_extension}"
    file_address = os.path.join(f"{folder_name}/", file_name)
    return file_address
