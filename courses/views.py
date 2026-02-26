from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from courses.models import Course
from assignments.models import Assignment
from users.decorators import instructor_required
from users.models import Profile
from .forms import CourseForm
from users.decorators import student_required

@login_required
def course_detail(request, course_id):
    if request.user.is_superuser:
        course = get_object_or_404(Course, id=course_id)

    elif request.user.profile.role == Profile.Role.INSTRUCTOR:
        course = get_object_or_404(
            Course,
            id=course_id,
            instructor=request.user
        )

    else:
        course = get_object_or_404(
            Course,
            id=course_id,
            students=request.user
        )

    assignments = Assignment.objects.filter(course=course).order_by("due_date")

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "assignments": assignments,
        }
    )

@login_required
@instructor_required
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user  # ✅ critical
            course.save()
            return redirect("instructor_dashboard")
    else:
        form = CourseForm()

    return render(
        request,
        "courses/create_course.html",
        {"form": form},
    )

@login_required
@student_required
def available_courses(request):
    enrolled_ids = request.user.enrolled_courses.values_list("id", flat=True)

    courses = Course.objects.exclude(id__in=enrolled_ids)

    return render(
        request,
        "courses/available_courses.html",
        {"courses": courses},
    )

@login_required
@student_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    course.students.add(request.user)

    return redirect("course_detail", course_id=course.id)


@login_required
@student_required
def leave_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    course.students.remove(request.user)

    return redirect("student_dashboard")