from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator to restrict access based on user role.
    Usage: @role_required(['admin', 'doctor'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to access this page.')
                return redirect('accounts:login')
            
            try:
                user_role = request.user.userprofile.role
                if user_role not in allowed_roles:
                    messages.error(request, 'You do not have permission to access this page.')
                    return redirect('accounts:dashboard')
            except:
                messages.error(request, 'Profile not found.')
                return redirect('accounts:login')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator to restrict access to admin only"""
    return role_required(['admin'])(view_func)


def doctor_required(view_func):
    """Decorator to restrict access to doctors only"""
    return role_required(['doctor'])(view_func)


def mother_required(view_func):
    """Decorator to restrict access to mothers only"""
    return role_required(['mother'])(view_func)
