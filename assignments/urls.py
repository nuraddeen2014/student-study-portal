from django.urls import path
from . import views

urlpatterns = [
    path('announcements/', views.view_announcements, name='view-announcements'),
    path('give/', views.give_assignment, name='give-assignment'),
    path('lecturer/', views.lecturer_assignments, name='lecturer-assignments'),
    path('dashboard/', views.lecturer_dashboard, name='lecturer-dashboard'),
    path('student/', views.student_assignments, name='student-assignments'),
    path('<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('<int:assignment_id>/submit/', views.submit_assignment, name='submit-assignment'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade-submission'),
    path('announcement/create/', views.create_announcement, name='create-announcement'),
]
