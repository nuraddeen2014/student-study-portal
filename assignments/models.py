from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    course_code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    lecturer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lecturer_assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code} - {self.title}"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_submissions'
    )
    content = models.TextField(blank=True)                 # optional text answer
    file = models.FileField(upload_to='submissions/', null=True, blank=True)  # optional file
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
