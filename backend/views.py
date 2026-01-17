from django.contrib.auth import logout as log_out
from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        print("user is logged in!")
        return render(request, "index.auth.html")
    else:
        print("dunno the user")
        return render(request, "index.html")


def logout(request):
    log_out(request)
    return redirect("/")
