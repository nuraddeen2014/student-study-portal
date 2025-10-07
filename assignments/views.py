from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm, GradeForm

# restrict lecturer actions only to staff users, check request.user.is_staff
# Admin will create lecturers — mark them as is_staff=True

@login_required
def give_assignment(request):
    # (Lecturer-only) create a new assignment
    if not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect('student-assignments')

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.lecturer = request.user
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('lecturer-assignments')
    else:
        form = AssignmentForm()
    return render(request, 'assignments/give_assignment.html', {'form': form})


@login_required
def lecturer_assignments(request):
    if not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect('student-assignments')

    assignments = Assignment.objects.filter(lecturer=request.user).order_by('-created_at')
    return render(request, 'assignments/lecturer_assignments.html', {'assignments': assignments})


@login_required
def student_assignments(request):
    # Students: view all assignments (later filter by enrollment)
    assignments = Assignment.objects.all().order_by('-created_at')
    return render(request, 'assignments/student_assignments.html', {'assignments': assignments})


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Student: check if they already submitted
    existing_submission = Submission.objects.filter(assignment=assignment, student=request.user).first()

    # Lecturer: see all submissions
    submissions = None
    if request.user.is_staff:
        submissions = Submission.objects.filter(assignment=assignment).order_by('-submitted_at')

    context = {
        'assignment': assignment,
        'existing_submission': existing_submission,
        'submissions': submissions
    }
    return render(request, 'assignments/assignment_detail.html', context)


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Optional deadline check
    if assignment.due_date and timezone.now() > assignment.due_date:
        messages.error(request, "This assignment is past its due date.")
        return redirect('assignment_detail', assignment_id=assignment.id)

    # Prevent duplicate submissions
    if Submission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.warning(request, "You have already submitted this assignment.")
        return redirect('assignment_detail', assignment_id=assignment.id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = SubmissionForm()

    return render(request, 'assignments/submit_assignment.html', {'form': form, 'assignment': assignment})


@login_required
def grade_submission(request, submission_id):
    # Lecturer grades a student's submission
    if not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect('student-assignments')

    submission = get_object_or_404(Submission, id=submission_id)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f"Submission by {submission.student.username} graded.")
            return redirect('assignment_detail', assignment_id=submission.assignment.id)
    else:
        form = GradeForm(instance=submission)

    return render(request, 'assignments/grade_submission.html', {'form': form, 'submission': submission})
