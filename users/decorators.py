from django.http import HttpResponseForbidden
from functools import wraps
from users.models import Profile


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
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.role != Profile.Role.INSTRUCTOR:
            return HttpResponseForbidden("Instructor access only")
        return view_func(request, *args, **kwargs)
    return _wrapped_view