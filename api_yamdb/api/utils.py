from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_confirmation_code(user):
    """Функция для отправки кода подтверждения"""
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Hallo from YaMDb',
        message=(
            f'Код подтверждения(confirmation_code): {confirmation_code}\n'
            'Используйте его для получения своего токена'
        ),
        from_email=None,
        recipient_list=[user.email],
    )
