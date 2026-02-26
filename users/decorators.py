from django.http import HttpResponseForbidden
from users.models import Profile

def student_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if request.user.profile.role != Profile.Role.STUDENT:
            return HttpResponseForbidden("Students only")

        return view_func(request, *args, **kwargs)
    return _wrapped


def instructor_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if request.user.profile.role != Profile.Role.INSTRUCTOR:
            return HttpResponseForbidden("Instructors only")

        return view_func(request, *args, **kwargs)
    return _wrapped