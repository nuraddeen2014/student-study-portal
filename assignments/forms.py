from django import forms
from .models import Assignment, Submission

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course_code', 'title', 'description', 'due_date']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course code'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assignment title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Assignment description'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your answer here...'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter grade'}),
        }
