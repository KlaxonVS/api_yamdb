from django.core.exceptions import ValidationError


def forbidden_username_check(name):
    """Делает невозможным использовать <<me>> как имя"""
    if name == 'me':
        raise ValidationError('Нельзя использовать "me" как username')
