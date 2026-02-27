from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import instructor_required
from assignments.models import Assignment, Submission
from assignments.forms import SubmissionForm
from users.models import Profile
from courses.models import Course
from .models import Assignment
from .forms import AssignmentForm
from datetime import time
from django.utils.timezone import make_aware
from django.utils import timezone

@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # --- Access control ---
    if request.user.profile.role == Profile.Role.STUDENT:
        if not assignment.course.students.filter(id=request.user.id).exists():
            return render(request, "403.html", status=403)

    submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    if request.method == "POST":
        if submission:
            return redirect("assignment_detail", assignment_id=assignment.id)

        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.assignment = assignment
            new_submission.student = request.user
            new_submission.save()
            return redirect("assignment_detail", assignment_id=assignment.id)
    else:
        form = SubmissionForm()

    return render(
        request,
        "assignments/assignment_detail.html",
        {
            "assignment": assignment,
            "submission": submission,
            "form": form,
        },
    )

@login_required
@instructor_required
def instructor_assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    submissions = assignment.submissions.select_related("student")

    if request.method == "POST":
        submission_id = request.POST.get("submission_id")
        grade = request.POST.get("grade")
        feedback = request.POST.get("feedback", "")

        submission = get_object_or_404(
            Submission,
            id=submission_id,
            assignment=assignment,
        )

        submission.grade = grade
        submission.feedback = feedback
        submission.save()

        return redirect(
            "instructor_assignment_detail",
            assignment_id=assignment.id,
        )

    return render(
        request,
        "assignments/instructor_assignment_detail.html",
        {
            "assignment": assignment,
            "submissions": submissions,
        },
    )

login_required
@instructor_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)

    if request.method == "POST":
        form = AssignmentForm(request.POST)

        if form.is_valid():
            assignment = form.save(commit=False)

            # 🔒 Force due time to 23:59
            selected_date = form.cleaned_data["due_date"]
            assignment.due_date = make_aware(
                timezone.datetime.combine(selected_date, time(23, 59))
            )

            assignment.course = course
            assignment.save()

            return redirect("course_detail", course_id=course.id)
    else:
        form = AssignmentForm()

    return render(
        request,
        "assignments/create_assignment.html",
        {
            "form": form,
            "course": course,
        },
    )