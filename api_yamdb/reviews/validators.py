from django.core.exceptions import ValidationError


def forbidden_username_check(name):
    if name == 'me':
        raise ValidationError('Нельзя использовать "me" как username')
