from django.http import HttpResponseForbidden
from functools import wraps


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not hasattr(user, "profile"):
            return HttpResponseForbidden("No profile")

        if user.profile.role != "student":
            return HttpResponseForbidden("Students only")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def instructor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not hasattr(user, "profile"):
            return HttpResponseForbidden("No profile")

        if user.profile.role != "instructor":
            return HttpResponseForbidden("Instructors only")

        return view_func(request, *args, **kwargs)

    return _wrapped_view