from django import forms
from .models import Task

class CreateNewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']