from django.http import HttpResponseForbidden

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("Not authenticated")

        if not hasattr(user, "profile"):
            return HttpResponseForbidden("Profile missing")

        if user.profile.role != "student":
            return HttpResponseForbidden("Students only")

        return view_func(request, *args, **kwargs)
    return wrapper


def instructor_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("Not authenticated")

        if not hasattr(user, "profile"):
            return HttpResponseForbidden("Profile missing")

        if user.profile.role != "instructor":
            return HttpResponseForbidden("Instructors only")

        return view_func(request, *args, **kwargs)
    return wrapper