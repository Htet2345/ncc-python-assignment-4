from django.core.validators import EmailValidator
from django.db import models
from .validators import validate_student_name, validate_student_phone


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'

    name = models.CharField(max_length=100, validators=[validate_student_name])
    email = models.EmailField(validators=[EmailValidator(allowlist=[])])
    gender = models.CharField(max_length=6, choices=Gender.choices)
    # A string keeps leading zeroes and international dialing prefixes.
    phone = models.CharField(max_length=30, validators=[validate_student_phone])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
