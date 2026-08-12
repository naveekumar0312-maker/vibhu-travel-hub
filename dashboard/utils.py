# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required, user_passes_test
# pyrefly: ignore [missing-import]
from django.shortcuts import redirect

def admin_required(view_func):
    """
    Decorator to ensure that the user is logged in and is a staff member.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/admin/'
    )
    return actual_decorator(view_func)
