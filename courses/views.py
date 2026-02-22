from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import instructor_required

@login_required
@instructor_required
def create_course(request):
    return render(request, "courses/create_course.html")