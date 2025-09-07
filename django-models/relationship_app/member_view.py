from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# helper decorator
def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            if request.user.userprofile.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@login_required
@role_required(allowed_roles=["Member"])
def member_view(request):
    return render(request, "member_page.html", {"user": request.user})
