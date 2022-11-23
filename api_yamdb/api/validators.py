from datetime import datetime

from django.core.exceptions import ValidationError


def year_validation(value):
    if value >= datetime.today().year:
        raise ValidationError(
            message=f'Год {value} больше текущего!',
            params={'value': value},
        )
