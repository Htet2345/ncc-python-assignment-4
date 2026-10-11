from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'gender', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student Name...', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student Email...', 'autocomplete': 'email'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student Phone...', 'type': 'tel', 'autocomplete': 'tel'}),
        }
        error_messages = {
            'name': {'required': 'Name is required.', 'max_length': 'Name is too long.'},
            'email': {'required': 'Email is required.', 'invalid': 'Enter a valid email address.'},
            'phone': {'required': 'Phone number is required.', 'max_length': 'Phone number is too long.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = [('', 'Choose gender'), *Student.Gender.choices]
        for name, field in self.fields.items():
            description = []
            if name in self.errors:
                field.widget.attrs['class'] += ' is-invalid'
                field.widget.attrs['aria-invalid'] = 'true'
                description.append(f'id_{name}_errors')
            if description:
                field.widget.attrs['aria-describedby'] = ' '.join(description)
