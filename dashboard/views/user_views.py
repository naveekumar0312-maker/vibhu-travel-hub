# pyrefly: ignore [missing-import]
from django.shortcuts import render
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User

@login_required(login_url='dashboard_login')
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users/list.html', {'users': users})
