from django.core.exceptions import ValidationError


def validate_username(name):
    """Делает невозможным использовать <<me>> как имя"""
    if name.lower() == 'me':
        raise ValidationError('Нельзя использовать <<me>> как username')