from django.contrib.auth import logout as log_out
from django.shortcuts import redirect


def logout(request):
    log_out(request)
    return redirect("/")
