from django.test import Client, TestCase
from django.urls import reverse
from .models import Student


class StudentCRUDTests(TestCase):
    def setUp(self):
        self.data = {'name': 'Alex', 'email': 'alex@gmail.com', 'gender': 'Female', 'phone': '0258963'}

    def test_complete_crud_flow(self):
        self.assertContains(self.client.get(reverse('students:list')), 'Student Lists')
        response = self.client.post(reverse('students:create'), self.data)
        self.assertRedirects(response, reverse('students:list'))
        student = Student.objects.get()
        self.assertEqual(student.phone, '0258963')
        self.assertContains(self.client.get(reverse('students:list')), 'alex@gmail.com')
        edit_url = reverse('students:edit', args=[student.pk])
        self.assertContains(self.client.get(edit_url), 'value="Alex"')
        updated = {**self.data, 'name': 'Alex update', 'email': 'alex_u@gmail.com'}
        self.assertRedirects(self.client.post(edit_url, updated), reverse('students:list'))
        student.refresh_from_db()
        self.assertEqual(student.name, 'Alex update')
        self.assertEqual(student.email, 'alex_u@gmail.com')
        self.assertRedirects(self.client.post(reverse('students:delete', args=[student.pk])), reverse('students:list'))
        self.assertFalse(Student.objects.exists())

    def test_invalid_create_does_not_save_and_keeps_input(self):
        for invalid in [{'email': 'invalid'}, {'gender': 'invalid'}, {'phone': 'letters'}, {'name': ''}]:
            response = self.client.post(reverse('students:create'), {**self.data, **invalid})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
            self.assertFalse(Student.objects.exists())

    def test_list_numbers_rows_from_one_after_deletion(self):
        first = Student.objects.create(**self.data)
        second = Student.objects.create(**{**self.data, 'name': 'Bob'})
        self.client.post(reverse('students:delete', args=[first.pk]))
        response = self.client.get(reverse('students:list'))
        self.assertContains(response, '<td>1</td><td>Bob</td>', html=True)

    def test_invalid_edit_does_not_change_record(self):
        student = Student.objects.create(**self.data)
        response = self.client.post(reverse('students:edit', args=[student.pk]), {**self.data, 'email': 'invalid'})
        self.assertEqual(response.status_code, 200)
        student.refresh_from_db()
        self.assertEqual(student.email, self.data['email'])

    def test_delete_get_never_deletes(self):
        student = Student.objects.create(**self.data)
        response = self.client.get(reverse('students:delete', args=[student.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Student.objects.filter(pk=student.pk).exists())

    def test_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        student = Student.objects.create(**self.data)
        for url in [reverse('students:create'), reverse('students:edit', args=[student.pk]), reverse('students:delete', args=[student.pk])]:
            self.assertEqual(client.post(url, self.data).status_code, 403)
        self.assertEqual(Student.objects.count(), 1)

    def test_missing_records_return_404(self):
        self.assertEqual(self.client.get(reverse('students:edit', args=[999])).status_code, 404)
        self.assertEqual(self.client.post(reverse('students:delete', args=[999])).status_code, 404)

    def test_student_names_are_escaped(self):
        Student.objects.create(**{**self.data, 'name': '<script>alert(1)</script>'})
        response = self.client.get(reverse('students:list'))
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')


class StudentValidationTests(TestCase):
    def setUp(self):
        self.data = {'name': 'Alex', 'email': 'alex@example.com', 'gender': 'Female', 'phone': '0258963'}

    def test_invalid_fields_are_rejected_on_create_and_edit(self):
        cases = {
            'name': ['', '   ', 'A', '12345', 'Alex123', 'Alex@Bob', '-Alex', 'A' * 101],
            'email': ['', 'alex', 'alex@', 'alex@example', 'alex@localhost', 'alex example@gmail.com', 'alex@@gmail.com'],
            'phone': ['', '12345', '1' * 16, 'abc123456', '123+456', '++123456', '123456.0'],
        }
        student = Student.objects.create(**self.data)
        for field, invalid_values in cases.items():
            for value in invalid_values:
                for operation in ['create', 'edit']:
                    with self.subTest(field=field, value=value, operation=operation):
                        url = reverse(f'students:{operation}', args=[student.pk] if operation == 'edit' else [])
                        response = self.client.post(url, {**self.data, field: value})
                        self.assertEqual(response.status_code, 200)
                        self.assertIn(field, response.context['form'].errors)
                        self.assertContains(response, f'id="id_{field}_errors"')
                        self.assertContains(response, 'aria-invalid="true"')
                        self.assertEqual(Student.objects.count(), 1)
                        student.refresh_from_db()
                        self.assertEqual(getattr(student, field), self.data[field])

    def test_valid_names_and_formatted_numbers(self):
        from .forms import StudentForm
        for name in ['Alex', 'Mary Jane', "O'Connor", 'Anne-Marie', 'Jos\u00e9', '\u1021\u1031\u102c\u1004\u103a']:
            with self.subTest(name=name):
                form = StudentForm(data={**self.data, 'name': name})
                self.assertTrue(form.is_valid(), form.errors)
        for phone in ['123456', '0258963', '+959 123-456-789', '(09) 123456789', '1' * 15]:
            with self.subTest(phone=phone):
                form = StudentForm(data={**self.data, 'phone': phone})
                self.assertTrue(form.is_valid(), form.errors)

    def test_email_format_and_whitespace(self):
        from .forms import StudentForm
        form = StudentForm(data={**self.data, 'name': '  Alex  ', 'email': ' alex+class@example.co.uk ', 'phone': ' 0258963 '})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['name'], 'Alex')
        self.assertEqual(form.cleaned_data['email'], 'alex+class@example.co.uk')
        self.assertEqual(form.cleaned_data['phone'], '0258963')

    def test_model_validation_uses_the_same_rules(self):
        from django.core.exceptions import ValidationError
        for field, value in [('name', 'Alex123'), ('email', 'alex@localhost'), ('phone', '123')]:
            with self.subTest(field=field):
                student = Student(**{**self.data, field: value})
                with self.assertRaises(ValidationError) as error:
                    student.full_clean()
                self.assertIn(field, error.exception.message_dict)
