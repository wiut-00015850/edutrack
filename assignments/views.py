from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import student_required

@login_required
@student_required
def submit_assignment(request):
    return render(request, "assignments/submit_assignment.html")