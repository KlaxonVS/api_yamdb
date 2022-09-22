from django.core.exceptions import ValidationError
from django.utils import timezone


def forbidden_username_check(name):
    """Делает невозможным использовать <<me>> как имя"""
    if name == 'me':
        raise ValidationError('Нельзя использовать "me" как username')


def validate_score_range(score):
    if score not in range(1, 11):
        raise ValidationError('Оценка должна быть целым числом от 1 до 10!')


def check_title_not_future(value):
    """Проверяет, что год выпуска не больше текущего"""
    if value > timezone.now().year:
        raise ValidationError(
            (f'Год выпуска не может быть больше текущего: {timezone.now().year}'
             f'Ваш год: {value}'),
        )