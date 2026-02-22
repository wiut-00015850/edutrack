from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError


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