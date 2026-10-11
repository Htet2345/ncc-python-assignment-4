"""Shared validation rules for student forms and Django admin."""
import re
import unicodedata
from django.core.exceptions import ValidationError


def validate_student_name(value):
    name = value.strip()
    categories = [unicodedata.category(char)[0] for char in name]
    if (
        sum(category == 'L' for category in categories) < 2
        or any(category not in ('L', 'M') and char not in " '-\u2019" for char, category in zip(name, categories))
        or not categories
        or categories[0] != 'L'
        or categories[-1] not in ('L', 'M')
    ):
        raise ValidationError(
            'Enter a valid name.',
            code='invalid_name',
        )


def validate_student_phone(value):
    phone = value.strip()
    if not re.fullmatch(r'\+?[0-9 ()-]+', phone) or not 6 <= len(re.findall(r'[0-9]', phone)) <= 15:
        raise ValidationError(
            'Enter a valid phone number.',
            code='invalid_phone',
        )
