from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse

def home(request):
    return HttpResponse("Logged in successfully")

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