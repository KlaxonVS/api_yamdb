from django.core.exceptions import ValidationError


def forbidden_username_check(name):
    """Делает невозможным использовать <<me>> как имя"""
    if name == 'me':
        raise ValidationError('Нельзя использовать "me" как username')


def validate_score_range(score):
    if score not in range(1, 11):
        raise ValidationError('Оценка должна быть целым числом от 1 до 10!')
