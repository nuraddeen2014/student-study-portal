from django.urls import path
from . import views

urlpatterns = [
    path('give/', views.give_assignment, name='give-assignment'),
    path('lecturer/', views.lecturer_assignments, name='lecturer-assignments'),
    path('student/', views.student_assignments, name='student-assignments'),
    path('<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('<int:assignment_id>/submit/', views.submit_assignment, name='submit-assignment'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade-submission'),
]
