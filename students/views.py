from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from .forms import StudentForm
from .models import Student


@require_http_methods(['GET'])
def student_list(request):
    return render(request, 'students/list.html', {'students': Student.objects.all()})


@require_http_methods(['GET', 'POST'])
def student_create(request):
    form = StudentForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('students:list')
    return render(request, 'students/form.html', {'form': form, 'title': 'Create Student'})


@require_http_methods(['GET', 'POST'])
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST if request.method == 'POST' else None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('students:list')
    return render(request, 'students/form.html', {'form': form, 'title': 'Edit Student'})


@require_POST
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('students:list')
