from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    role = request.user.profile.role

    if role == "student":
        return redirect("student_dashboard")
    elif role == "instructor":
        return redirect("instructor_dashboard")
    else:
        return redirect("/admin/")

def health_check(request):
    try:
        db_conn = connections["default"]
        db_conn.cursor()
        db_status = "connected"
    except OperationalError:
        db_status = "error"

    return JsonResponse(
        {
            "status": "ok",
            "database": db_status,
        }
    )