#put it to your app/shared/decorators.py and than import when required

from django.core.exceptions import PermissionDenied
from .models import Class

def superuser_only(function):
    """
    Limit view to superusers only.

    Usage:
    --------------------------------------------------------------------------
    @superuser_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------

    or in urls:

    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', is_staff(my_view)),
    )
    --------------------------------------------------------------------------
    """
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("These Pages are only for administrator")
        return function(request, *args, **kwargs)
    return _inner

def class_teacher_only(function):
    def _inner(request, *args, **kwargs):
        class_t_o = Class.objects.filter(class_teacher= request.user).first()
        if (not class_t_o) or request.user.is_superuser:
            raise PermissionDenied("These Pages are only for administrator")
        return function(request, *args, **kwargs)
    return _inner
