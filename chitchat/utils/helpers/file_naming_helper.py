import os, uuid


def create_unique_filename(instance, filename):
    file_extension = filename.split(".")[-1]
    if hasattr(instance, "user"):
        user_email_splitted = instance.user.email.split("@")[0]
        name = f"{user_email_splitted}_{instance.user.id}"
        folder_name = "profile_pictures"
    elif hasattr(instance, "group_name"):
        group_name_replaced = instance.group_name.replace(" ", "_")
        name = f"{group_name_replaced}_{instance.group_admin.id}"
        folder_name = "group_avatars"
    elif hasattr(instance, "content_type"):
        if hasattr(instance.content_type.startswith("image")):
            name = f"{instance.uploaded_by.email}_{uuid.uuid4().hex}"
            folder_name = "message_attachments/images"
        elif hasattr(instance.content_type.startswith("video")):
            name = f"{instance.uploaded_by.email}_{uuid.uuid4().hex}"
            folder_name = "message_attachments/videos"
        elif hasattr(instance.content_type.startswith("audios")):
            name = f"{instance.uploaded_by.email}_{uuid.uuid4().hex}"
            folder_name = "message_attachments/audios"
        elif hasattr(instance.content_type.startswith("documents")):
            name = f"{instance.uploaded_by.email}_{uuid.uuid4().hex}"
            folder_name = "message_attachments/documents"
        else:
            name = f"{instance.uploaded_by.email}_{uuid.uuid4().hex}"
            folder_name = "message_attachments/others"
    else:
        name = f"unknown_{uuid.uuid4().hex}"
        folder_name = "uploads"

    file_name = f"{name}.{file_extension}"
    file_address = os.path.join(f"{folder_name}/", file_name)
    return file_address
