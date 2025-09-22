from django.core.exceptions import ValidationError


def validate_file_size(value):

    max_allowed_size = 10 * 1024 * 1024  # 10MB file support
    if value.size > max_allowed_size:
        raise ValidationError(
            f"File size should not exceed more than 10MB. Current file size: {round(value.size / (1024 * 1024), 2)}MB"
        )
