from django.core.validators import ValidationError


def validate_image_size(image):
    filesize = image.file.size
    megabyte_limit = 5.0

    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Max image size is {megabyte_limit}MB!!!")
