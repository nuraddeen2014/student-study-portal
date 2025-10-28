from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
    
    @property
    def image_url(self):
        """Returns a course-specific image URL based on the course code."""
        image_urls = {
            'csc101': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80',
            'mat101': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=800&q=80',
            'phy101': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=800&q=80',
            'chm101': 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80',
            'bio101': 'https://images.unsplash.com/photo-1576086213369-97a306d36557?auto=format&fit=crop&w=800&q=80',
            'eng101': 'https://images.unsplash.com/photo-1581094283645-9f6fbcef9cab?auto=format&fit=crop&w=800&q=80',
            'lit101': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=800&q=80',
            'his101': 'https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=800&q=80',
        }
        return image_urls.get(
            self.course_code.lower(),
            'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80'
        )

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


class Announcement(models.Model):
    """Simple announcement model for lecturers to post quick notices/resources."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def expires_at(self):
        """Datetime when this announcement will expire (24 hours after creation)."""
        if self.created_at is None:
            return None
        return self.created_at + timedelta(hours=24)

    def expires_in(self):
        """Human readable time until expiry. Returns a short string like 'Expires in 5h 3m' or 'Expired'."""
        exp = self.expires_at
        if exp is None:
            return ""
        now = timezone.now()
        # convert both to same timezone-aware representation
        try:
            now = timezone.localtime(now)
            exp_local = timezone.localtime(exp)
        except Exception:
            exp_local = exp

        delta = exp_local - now
        seconds = int(delta.total_seconds())
        if seconds <= 0:
            return "Expired"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if hours > 0:
            return f"Expires in {hours}h {minutes}m"
        return f"Expires in {minutes}m"

    def __str__(self):
        return f"{self.title} by {self.author.username}"
