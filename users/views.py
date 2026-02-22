from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import student_required, instructor_required


@login_required
def role_redirect(request):
    role = request.user.profile.role

    if role == "student":
        return redirect("student_dashboard")
    elif role == "instructor":
        return redirect("instructor_dashboard")

    return render(request, "users/invalid_role.html", status=403)


@login_required
@student_required
def student_dashboard(request):
    return render(request, "users/student_dashboard.html")


@login_required
@instructor_required
def instructor_dashboard(request):
    return render(request, "users/instructor_dashboard.html")